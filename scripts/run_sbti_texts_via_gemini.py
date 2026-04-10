#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
import threading
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.1-pro-preview"
SECTION_ORDER = [
    "ui",
    "dimensionMeta",
    "questions",
    "specialQuestions",
    "typeLibrary",
    "dimExplanations",
]


def load_local_env(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def ensure_api_key() -> str:
    key = str(os.getenv("GEMINI_API_KEY", "")).strip()
    if not key:
        raise RuntimeError("Missing GEMINI_API_KEY. Please export GEMINI_API_KEY before running this script.")
    return key


def resolve_model_name() -> str:
    configured = str(os.getenv("GEMINI_MODEL", "")).strip()
    return configured or DEFAULT_MODEL


def load_prompts(*, system_prompt_path: Path, rewrite_prompt_path: Path) -> tuple[str, str]:
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
    rewrite_template = rewrite_prompt_path.read_text(encoding="utf-8")
    if "{source_text}" not in rewrite_template or "{draft_text}" not in rewrite_template:
        raise ValueError("Rewrite prompt template must include {source_text} and {draft_text} placeholders.")
    return system_prompt, rewrite_template


def extract_text_from_response(response: Any) -> str:
    text = str(getattr(response, "text", "") or "").strip()
    if text:
        return text

    candidates = getattr(response, "candidates", None)
    if candidates:
        chunks: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) if content else None
            if not parts:
                continue
            for part in parts:
                maybe_text = getattr(part, "text", None)
                if maybe_text:
                    chunks.append(str(maybe_text))
        if chunks:
            return "\n".join(chunks).strip()
    return ""


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        lines = stripped.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return stripped


def scan_until_matching(text: str, start_index: int, open_char: str, close_char: str) -> int:
    depth = 0
    quote_char: str | None = None
    escaped = False

    for index in range(start_index, len(text)):
        char = text[index]
        if quote_char:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote_char:
                quote_char = None
            continue

        if char in {"'", '"'}:
            quote_char = char
            continue

        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return index

    raise ValueError(f"Could not find matching {close_char} for {open_char} at index {start_index}")


def split_top_level_properties(body: str) -> list[str]:
    entries: list[str] = []
    start = 0
    brace_depth = 0
    bracket_depth = 0
    quote_char: str | None = None
    escaped = False

    for index, char in enumerate(body):
        if quote_char:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote_char:
                quote_char = None
            continue

        if char in {"'", '"'}:
            quote_char = char
            continue

        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        elif char == "," and brace_depth == 0 and bracket_depth == 0:
            entry = body[start:index].strip()
            if entry:
                entries.append(entry)
            start = index + 1

    tail = body[start:].strip()
    if tail:
        entries.append(tail)
    return entries


def find_top_level_colon(entry: str) -> int:
    brace_depth = 0
    bracket_depth = 0
    quote_char: str | None = None
    escaped = False

    for index, char in enumerate(entry):
        if quote_char:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote_char:
                quote_char = None
            continue

        if char in {"'", '"'}:
            quote_char = char
            continue

        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        elif char == ":" and brace_depth == 0 and bracket_depth == 0:
            return index

    raise ValueError(f"Could not find top-level colon in property: {entry[:80]}")


def extract_root_sections(source_text: str) -> dict[str, str]:
    assign_marker = "window.SBTI_TEXTS"
    marker_index = source_text.find(assign_marker)
    if marker_index == -1:
        raise ValueError("Input file does not contain window.SBTI_TEXTS")

    object_start = source_text.find("{", marker_index)
    if object_start == -1:
        raise ValueError("Could not find root object start")

    object_end = scan_until_matching(source_text, object_start, "{", "}")
    body = source_text[object_start + 1:object_end]

    sections: dict[str, str] = {}
    for entry in split_top_level_properties(body):
        colon_index = find_top_level_colon(entry)
        key = entry[:colon_index].strip().strip('"').strip("'")
        sections[key] = entry.strip().rstrip(",")
    return sections


def normalize_property_block(block: str) -> str:
    return textwrap.dedent(block).strip().rstrip(",")


def assemble_sections(sections: dict[str, str]) -> str:
    ordered_blocks = []
    for key in SECTION_ORDER:
        if key not in sections:
            raise ValueError(f"Missing section in assembled output: {key}")
        block = normalize_property_block(sections[key])
        ordered_blocks.append(textwrap.indent(block, "  "))
    return "window.SBTI_TEXTS = {\n" + ",\n\n".join(ordered_blocks) + "\n};\n"


def validate_section_output(*, section_name: str, text: str) -> str:
    cleaned = strip_code_fences(text)
    if "window.SBTI_TEXTS" in cleaned:
        sections = extract_root_sections(cleaned)
        block = sections.get(section_name)
        if not block:
            raise RuntimeError(f"Gemini returned a full file, but section {section_name} was missing.")
        return normalize_property_block(block)

    pattern = re.compile(rf"(^|\n)\s*{re.escape(section_name)}\s*:", re.MULTILINE)
    match = pattern.search(cleaned)
    if not match:
        raise RuntimeError(f"Gemini response does not look like a `{section_name}` property block.")
    return normalize_property_block(cleaned[match.start():])


class GeminiClient:
    def __init__(self, *, api_key: str, model_name: str) -> None:
        self._api_key = api_key
        self._model_name = model_name
        self._client = None
        self._lock = threading.Lock()

    def _ensure_client(self):
        with self._lock:
            if self._client is not None:
                return self._client
            from google import genai

            self._client = genai.Client(api_key=self._api_key)
            return self._client

    def preflight(self) -> None:
        client = self._ensure_client()
        response = client.models.generate_content(
            model=self._model_name,
            contents='Return exactly this string: ok',
        )
        text = extract_text_from_response(response).strip().lower()
        if "ok" not in text:
            raise RuntimeError(f"Gemini preflight failed for model {self._model_name}: {text[:200]}")

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        client = self._ensure_client()
        response = client.models.generate_content(
            model=self._model_name,
            contents=user_prompt,
            config={"system_instruction": system_prompt},
        )
        text = extract_text_from_response(response)
        if not text:
            raise RuntimeError("Gemini returned empty response text.")
        return text


def build_section_draft_prompt(*, section_name: str, source_block: str) -> str:
    return (
        f"请只重写 SBTI 文案资源里的 `{section_name}` 这个片段。\n"
        "要求：\n"
        "1. 只改用户可见文案，不改 key 名、对象层级、数组长度、题目 id、人格 code、选项 value、图片路径。\n"
        "2. 保留原项目的网感、梗感、丧感和轻微攻击性，但要更稳、更自然，少一点生硬 AI 味。\n"
        "3. 直接输出一个 JS 对象属性片段，必须以原 section 名开头，不要输出完整文件，不要 markdown 围栏，不要解释。\n"
        f"4. 这次只能处理 `{section_name}`，不要擅自补其他 section。\n\n"
        "原始片段如下：\n"
        f"{source_block}"
    )


def build_section_rewrite_prompt(
    *,
    section_name: str,
    source_block: str,
    draft_block: str,
    rewrite_template: str,
) -> str:
    prompt = rewrite_template.replace("{source_text}", source_block).replace("{draft_text}", draft_block)
    return (
        f"你现在只允许处理 `{section_name}` 这个 section。\n"
        "输出必须是单个 JS 对象属性片段，必须以原 section 名开头，不要输出完整文件，不要解释。\n\n"
        f"{prompt}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite SBTI text resources via Gemini.")
    parser.add_argument(
        "--input",
        default=str(PROJECT_ROOT / "data" / "sbti-texts.js"),
        help="Path to the source sbti-texts.js file.",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "data" / "sbti-texts.gemini.js"),
        help="Path to write the Gemini candidate file.",
    )
    parser.add_argument(
        "--system-prompt",
        default=str(PROJECT_ROOT / "prompts" / "sbti_texts_rewrite_system.txt"),
        help="System prompt file path.",
    )
    parser.add_argument(
        "--rewrite-prompt",
        default=str(PROJECT_ROOT / "prompts" / "sbti_texts_rewrite_pass.txt"),
        help="Second-pass prompt template file path.",
    )
    parser.add_argument(
        "--single-pass",
        action="store_true",
        help="Only run one rewrite pass for each section.",
    )
    args = parser.parse_args()

    load_local_env(PROJECT_ROOT / ".env")

    input_path = Path(args.input)
    output_path = Path(args.output)
    system_prompt_path = Path(args.system_prompt)
    rewrite_prompt_path = Path(args.rewrite_prompt)

    if not input_path.exists():
        raise RuntimeError(f"Input file not found: {input_path}")

    api_key = ensure_api_key()
    model_name = resolve_model_name()
    source_text = input_path.read_text(encoding="utf-8")
    system_prompt, rewrite_template = load_prompts(
        system_prompt_path=system_prompt_path,
        rewrite_prompt_path=rewrite_prompt_path,
    )

    source_sections = extract_root_sections(source_text)
    missing_sections = [name for name in SECTION_ORDER if name not in source_sections]
    if missing_sections:
        raise RuntimeError(f"Input file is missing sections: {', '.join(missing_sections)}")

    client = GeminiClient(api_key=api_key, model_name=model_name)
    print(f"[preflight] model={model_name}")
    client.preflight()
    print("[preflight] ok")

    generated_sections: dict[str, str] = {}
    total = len(SECTION_ORDER)
    for index, section_name in enumerate(SECTION_ORDER, start=1):
        source_block = source_sections[section_name]
        print(f"[{index}/{total}] drafting {section_name} ...")
        draft_prompt = build_section_draft_prompt(section_name=section_name, source_block=source_block)
        draft_block = validate_section_output(
            section_name=section_name,
            text=client.generate_text(system_prompt=system_prompt, user_prompt=draft_prompt),
        )

        if args.single_pass:
            generated_sections[section_name] = draft_block
            print(f"[{index}/{total}] {section_name} ok (single pass)")
            continue

        print(f"[{index}/{total}] polishing {section_name} ...")
        rewrite_prompt = build_section_rewrite_prompt(
            section_name=section_name,
            source_block=source_block,
            draft_block=draft_block,
            rewrite_template=rewrite_template,
        )
        final_block = validate_section_output(
            section_name=section_name,
            text=client.generate_text(system_prompt=system_prompt, user_prompt=rewrite_prompt),
        )
        generated_sections[section_name] = final_block
        print(f"[{index}/{total}] {section_name} ok")

    final_text = assemble_sections(generated_sections)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_text, encoding="utf-8")
    print(f"Wrote Gemini candidate to: {output_path}")
    print(f"Model: {model_name}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
