#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
import threading
import time
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
DEFAULT_PLACEHOLDER_TOKEN = "__GEMINI__"
SECTION_ORDER = [
    "ui",
    "dimensionMeta",
    "questions",
    "specialQuestions",
    "typeLibrary",
    "dimExplanations",
]
SECTION_BATCH_SIZES = {
    "questions": 6,
    "typeLibrary": 4,
}
MAX_RETRIES = 2
RETRY_BASE_DELAY_SECONDS = 2.0


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


def split_property_block(block: str) -> tuple[str, str]:
    cleaned = normalize_property_block(block)
    colon_index = find_top_level_colon(cleaned)
    key = cleaned[:colon_index].strip().strip('"').strip("'")
    value = cleaned[colon_index + 1:].strip()
    return key, value


def split_property_value_entries(block: str) -> tuple[str, list[str]]:
    _, value = split_property_block(block)
    if not value:
        raise ValueError("Property block has empty value")

    start_char = value[0]
    if start_char == "[":
        kind = "array"
        end_char = "]"
    elif start_char == "{":
        kind = "object"
        end_char = "}"
    else:
        raise ValueError(f"Unsupported batched property value: {value[:40]}")

    end_index = scan_until_matching(value, 0, start_char, end_char)
    inner_body = value[1:end_index].strip()
    entries = split_top_level_properties(inner_body) if inner_body else []
    return kind, entries


def assemble_property_entries(*, section_name: str, kind: str, entries: list[str]) -> str:
    if kind == "array":
        open_char, close_char = "[", "]"
    elif kind == "object":
        open_char, close_char = "{", "}"
    else:
        raise ValueError(f"Unsupported property kind: {kind}")

    if not entries:
        return f"{section_name}: {open_char}{close_char}"

    rendered_entries = [
        textwrap.indent(normalize_property_block(entry), "  ")
        for entry in entries
    ]
    return f"{section_name}: {open_char}\n" + ",\n".join(rendered_entries) + f"\n{close_char}"


def chunked(items: list[str], size: int) -> list[list[str]]:
    if size <= 0:
        return [items]
    return [items[index:index + size] for index in range(0, len(items), size)]


def build_section_batches(*, section_name: str, source_block: str) -> list[str]:
    batch_size = SECTION_BATCH_SIZES.get(section_name)
    if not batch_size:
        return [normalize_property_block(source_block)]

    kind, entries = split_property_value_entries(source_block)
    return [
        assemble_property_entries(section_name=section_name, kind=kind, entries=batch_entries)
        for batch_entries in chunked(entries, batch_size)
    ]


def merge_section_batches(*, section_name: str, generated_blocks: list[str]) -> str:
    if not generated_blocks:
        raise ValueError(f"No generated blocks to merge for section {section_name}")
    if len(generated_blocks) == 1:
        return normalize_property_block(generated_blocks[0])

    merged_kind: str | None = None
    merged_entries: list[str] = []
    for block in generated_blocks:
        kind, entries = split_property_value_entries(block)
        if merged_kind is None:
            merged_kind = kind
        elif merged_kind != kind:
            raise ValueError(f"Mismatched batch kinds for section {section_name}: {merged_kind} vs {kind}")
        merged_entries.extend(entries)

    return assemble_property_entries(section_name=section_name, kind=merged_kind or "array", entries=merged_entries)


def tokenize_js_like(text: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    quote_char: str | None = None
    escaped = False
    literal_chars: list[str] = []

    for char in text:
        if quote_char is not None:
            if escaped:
                literal_chars.append(char)
                escaped = False
                continue
            if char == "\\":
                literal_chars.append(char)
                escaped = True
                continue
            if char == quote_char:
                literal = "".join(literal_chars)
                tokens.append(("str", f"{quote_char}{literal}{quote_char}"))
                quote_char = None
                literal_chars = []
                continue
            literal_chars.append(char)
            continue

        if char in {"'", '"'}:
            quote_char = char
            literal_chars = []
            continue
        if char.isspace():
            continue
        tokens.append(("sym", char))

    if quote_char is not None:
        raise ValueError("Unterminated string literal while tokenizing block.")

    return tokens


def block_has_placeholder(block: str, *, placeholder_token: str) -> bool:
    return placeholder_token in block


def assert_locked_text_preserved(
    *,
    source_block: str,
    generated_block: str,
    placeholder_token: str,
    label: str,
) -> None:
    if placeholder_token in generated_block:
        raise RuntimeError(f"{label} still contains placeholder token {placeholder_token!r}.")

    source_tokens = tokenize_js_like(source_block)
    generated_tokens = tokenize_js_like(generated_block)

    if len(source_tokens) != len(generated_tokens):
        raise RuntimeError(
            f"{label} changed the structure of the block. "
            "Only placeholder strings are allowed to change."
        )

    for index, ((source_kind, source_value), (generated_kind, generated_value)) in enumerate(
        zip(source_tokens, generated_tokens),
        start=1,
    ):
        if source_kind != generated_kind:
            raise RuntimeError(
                f"{label} changed the block structure near token {index}. "
                "Only placeholder strings are allowed to change."
            )
        if source_kind == "str" and placeholder_token in source_value:
            continue
        if source_value != generated_value:
            raise RuntimeError(
                f"{label} changed locked text outside placeholder values near token {index}. "
                "Only placeholder strings are allowed to change."
            )


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


def build_section_draft_prompt_v2(
    *,
    section_name: str,
    source_block: str,
    placeholder_token: str,
    batch_note: str = "",
) -> str:
    note = batch_note or (
        "Only replace placeholder string values in this block. Do not add, remove, reorder, or merge entries."
    )
    return (
        f"Fill only the new-copy placeholders inside the `{section_name}` section of this SBTI text resource.\n"
        "Requirements:\n"
        f"1. Only replace string values that contain the placeholder token `{placeholder_token}`.\n"
        "2. Every non-placeholder string must stay unchanged.\n"
        "3. Do not change key names, object nesting, array length, question ids, type codes, option values, or image paths.\n"
        "4. Keep the existing voice: internet-native, funny, bleak, a little mean, but still readable and natural.\n"
        "5. Each placeholder string may contain a short instruction after the token. Use it to write the final user-facing Chinese copy.\n"
        "6. Output exactly one JavaScript property block starting with the original section name.\n"
        "7. Do not output a full file. Do not output Markdown fences. Do not explain anything.\n"
        f"8. {note}\n\n"
        "Source block:\n"
        f"{source_block}"
    )


def build_section_rewrite_prompt_v2(
    *,
    section_name: str,
    source_block: str,
    draft_block: str,
    rewrite_template: str,
    placeholder_token: str,
    batch_note: str = "",
) -> str:
    note = batch_note or (
        "Only replace placeholder string values in this block. Do not add, remove, reorder, or merge entries."
    )
    prompt = rewrite_template.replace("{source_text}", source_block).replace("{draft_text}", draft_block)
    return (
        f"You may only work on the `{section_name}` section.\n"
        f"Only placeholder string values containing `{placeholder_token}` may change.\n"
        "All existing non-placeholder strings are locked and must remain unchanged.\n"
        "Output exactly one JavaScript property block starting with the original section name.\n"
        "Do not output a full file. Do not explain anything.\n"
        f"{note}\n\n"
        f"{prompt}"
    )


def call_with_retries(*, label: str, fn):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return fn()
        except Exception:
            if attempt >= MAX_RETRIES:
                raise
            delay = RETRY_BASE_DELAY_SECONDS * (attempt + 1)
            print(f"[retry] {label} failed, retrying in {delay:.0f}s ...")
            time.sleep(delay)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill new SBTI placeholder texts via Gemini.")
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
    parser.add_argument(
        "--model",
        default=None,
        help="Override Gemini model name for this run.",
    )
    parser.add_argument(
        "--placeholder-token",
        default=DEFAULT_PLACEHOLDER_TOKEN,
        help="Only string values containing this token will be sent to Gemini for filling.",
    )
    args = parser.parse_args()

    load_local_env(PROJECT_ROOT / ".env")

    input_path = Path(args.input)
    output_path = Path(args.output)
    system_prompt_path = Path(args.system_prompt)
    rewrite_prompt_path = Path(args.rewrite_prompt)

    if not input_path.exists():
        raise RuntimeError(f"Input file not found: {input_path}")

    model_name = str(args.model or resolve_model_name()).strip()
    placeholder_token = str(args.placeholder_token or "").strip()
    if not placeholder_token:
        raise RuntimeError("Placeholder token cannot be empty.")
    source_text = input_path.read_text(encoding="utf-8")
    system_prompt, rewrite_template = load_prompts(
        system_prompt_path=system_prompt_path,
        rewrite_prompt_path=rewrite_prompt_path,
    )

    source_sections = extract_root_sections(source_text)
    missing_sections = [name for name in SECTION_ORDER if name not in source_sections]
    if missing_sections:
        raise RuntimeError(f"Input file is missing sections: {', '.join(missing_sections)}")

    prepared_sections: list[tuple[str, list[str]]] = []
    placeholder_batches = 0
    for section_name in SECTION_ORDER:
        source_batches = build_section_batches(section_name=section_name, source_block=source_sections[section_name])
        prepared_sections.append((section_name, source_batches))
        placeholder_batches += sum(
            1 for block in source_batches
            if block_has_placeholder(block, placeholder_token=placeholder_token)
        )

    if placeholder_batches == 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(input_path.read_bytes())
        print(
            f"No placeholder token {placeholder_token!r} found. "
            f"Copied input unchanged to: {output_path}"
        )
        return 0

    api_key = ensure_api_key()
    client = GeminiClient(api_key=api_key, model_name=model_name)
    print(f"[preflight] model={model_name}")
    client.preflight()
    print("[preflight] ok")
    print(f"[plan] placeholder batches={placeholder_batches}, token={placeholder_token}")

    generated_sections: dict[str, str] = {}
    total = len(SECTION_ORDER)
    for index, (section_name, source_batches) in enumerate(prepared_sections, start=1):
        generated_batches: list[str] = []

        for batch_index, source_block in enumerate(source_batches, start=1):
            batch_suffix = ""
            batch_note = ""
            if len(source_batches) > 1:
                batch_suffix = f" batch {batch_index}/{len(source_batches)}"
                batch_note = (
                    f"This is only batch {batch_index}/{len(source_batches)} of the `{section_name}` section. "
                    "Only fill placeholders in the entries shown here, and keep the same count and order."
                )

            if not block_has_placeholder(source_block, placeholder_token=placeholder_token):
                generated_batches.append(normalize_property_block(source_block))
                print(f"[{index}/{total}] {section_name}{batch_suffix} locked (no placeholders)")
                continue

            print(f"[{index}/{total}] drafting {section_name}{batch_suffix} ...")
            draft_prompt = build_section_draft_prompt_v2(
                section_name=section_name,
                source_block=source_block,
                placeholder_token=placeholder_token,
                batch_note=batch_note,
            )
            draft_block = call_with_retries(
                label=f"{section_name}{batch_suffix} draft",
                fn=lambda prompt=draft_prompt: validate_section_output(
                    section_name=section_name,
                    text=client.generate_text(system_prompt=system_prompt, user_prompt=prompt),
                ),
            )
            assert_locked_text_preserved(
                source_block=source_block,
                generated_block=draft_block,
                placeholder_token=placeholder_token,
                label=f"{section_name}{batch_suffix} draft",
            )

            if args.single_pass:
                generated_batches.append(draft_block)
                print(f"[{index}/{total}] {section_name}{batch_suffix} ok (single pass)")
                continue

            print(f"[{index}/{total}] polishing {section_name}{batch_suffix} ...")
            rewrite_prompt = build_section_rewrite_prompt_v2(
                section_name=section_name,
                source_block=source_block,
                draft_block=draft_block,
                rewrite_template=rewrite_template,
                placeholder_token=placeholder_token,
                batch_note=batch_note,
            )
            final_block = call_with_retries(
                label=f"{section_name}{batch_suffix} polish",
                fn=lambda prompt=rewrite_prompt: validate_section_output(
                    section_name=section_name,
                    text=client.generate_text(system_prompt=system_prompt, user_prompt=prompt),
                ),
            )
            assert_locked_text_preserved(
                source_block=source_block,
                generated_block=final_block,
                placeholder_token=placeholder_token,
                label=f"{section_name}{batch_suffix} polish",
            )
            generated_batches.append(final_block)
            print(f"[{index}/{total}] {section_name}{batch_suffix} ok")

        generated_sections[section_name] = merge_section_batches(
            section_name=section_name,
            generated_blocks=generated_batches,
        )

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
