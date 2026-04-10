#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import threading
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.1-pro-preview"


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


def validate_generated_file(text: str) -> str:
    cleaned = strip_code_fences(text)
    if not cleaned.lstrip().startswith("window.SBTI_TEXTS ="):
        raise RuntimeError("Gemini response does not look like a complete sbti-texts.js file.")
    return cleaned.rstrip() + "\n"


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


def build_draft_prompt(source_text: str) -> str:
    return (
        "请基于下面这份 SBTI 文案资源文件给出一版完整重写。\n"
        "要求：\n"
        "1. 只改文本，不改 key 名、对象层级、数组长度、题目 id、人格 code、选项 value。\n"
        "2. 保留原项目的网感、梗感、丧感和轻微攻击性，但要更稳、更自然，少一点生硬 AI 味。\n"
        "3. 题干、选项、人格简介、维度说明、按钮、提示语都要一起处理。\n"
        "4. 直接输出完整 JS 文件，不要解释，不要 markdown 围栏。\n\n"
        "源文件如下：\n"
        f"{source_text}"
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
    args = parser.parse_args()

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

    client = GeminiClient(api_key=api_key, model_name=model_name)
    client.preflight()

    draft_prompt = build_draft_prompt(source_text)
    draft_text = validate_generated_file(
        client.generate_text(system_prompt=system_prompt, user_prompt=draft_prompt)
    )

    rewrite_prompt = (
        rewrite_template
        .replace("{source_text}", source_text)
        .replace("{draft_text}", draft_text)
    )
    final_text = validate_generated_file(
        client.generate_text(system_prompt=system_prompt, user_prompt=rewrite_prompt)
    )

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
