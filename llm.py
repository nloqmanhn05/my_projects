"""
llm.py - the ONLY file that talks to Gemini.

Everything else calls:
    ask_json(prompt, system=None, schema=None) -> dict | list

What it does for you:
  * reads GEMINI_API_KEY from .env
  * asks Gemini to answer in JSON
  * retries on rate limits (429) and server errors (5xx), waiting longer each time
  * if the answer is not valid JSON, asks once more
  * raises LLMError if it still fails (the pipeline turns that into NEEDS_REVIEW)

Test it:   python llm.py
Offline:   set LLM_FAKE=1 to test the pipeline without calling Gemini.
"""
import json
import os
import re
import time

from dotenv import load_dotenv

import config

load_dotenv()


class LLMError(Exception):
    """Raised when Gemini cannot give a usable answer."""


_client = None


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise LLMError("GEMINI_API_KEY not found. Put it in the .env file.")
        from google import genai
        from google.genai import types
        _client = genai.Client(
            api_key=key,
            http_options=types.HttpOptions(timeout=config.REQUEST_TIMEOUT_MS),
        )
    return _client


def _extract_json(text):
    """Parse JSON even if the model wrapped it in ```json fences or added words."""
    if text is None:
        raise ValueError("empty response")
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.IGNORECASE).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        # last resort: take from the first { or [ to the last } or ]
        starts = [i for i in (t.find("{"), t.find("[")) if i != -1]
        if not starts:
            raise
        start = min(starts)
        end = max(t.rfind("}"), t.rfind("]"))
        return json.loads(t[start:end + 1])


def _call_gemini(prompt, system, schema):
    """One raw call. Retries on rate limits and server errors. Returns text."""
    from google.genai import errors, types

    cfg = dict(
        temperature=config.TEMPERATURE,
        max_output_tokens=config.MAX_OUTPUT_TOKENS,
        response_mime_type="application/json",
    )
    if system:
        cfg["system_instruction"] = system
    if schema:
        cfg["response_schema"] = schema
    config_obj = types.GenerateContentConfig(**cfg)

    last_error = None
    for attempt in range(config.MAX_RETRIES + 1):
        try:
            resp = _get_client().models.generate_content(
                model=config.MODEL, contents=prompt, config=config_obj
            )
            text = resp.text
            if not text:
                raise LLMError(f"Gemini returned no text (finish reason: "
                               f"{getattr(resp.candidates[0], 'finish_reason', '?') if resp.candidates else 'no candidates'})")
            return text
        except errors.APIError as e:
            last_error = e
            code = getattr(e, "code", None)
            retryable = code == 429 or (isinstance(code, int) and 500 <= code < 600)
            if not retryable or attempt == config.MAX_RETRIES:
                raise LLMError(f"Gemini error {code}: {e}") from e
            wait = config.RETRY_BASE_SECONDS * (2 ** attempt)
            print(f"  [llm] error {code}, retry {attempt + 1}/{config.MAX_RETRIES} in {wait}s")
            time.sleep(wait)
    raise LLMError(f"Gemini failed: {last_error}")


def _fake(prompt):
    """Offline stand-in so you can test the pipeline without an API key."""
    return {"fake": True, "note": "LLM_FAKE=1, no real call was made"}


def ask_json(prompt, system=None, schema=None):
    """
    Send a prompt, get parsed JSON back (dict or list).
    Raises LLMError if it cannot.
    """
    if os.getenv("LLM_FAKE") == "1":
        return _fake(prompt)

    current = prompt
    for attempt in range(config.JSON_REPAIR_ATTEMPTS + 1):
        text = _call_gemini(current, system, schema)
        try:
            return _extract_json(text)
        except (json.JSONDecodeError, ValueError) as e:
            if attempt == config.JSON_REPAIR_ATTEMPTS:
                raise LLMError(f"Answer was not valid JSON: {e}. Got: {text[:200]!r}") from e
            current = (prompt + "\n\nYour previous answer was not valid JSON. "
                       "Reply again with ONLY valid JSON, no extra text.")
    raise LLMError("unreachable")


# ----------------------------------------------------------------------
# Self-test. Run:  python llm.py
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # 1) parser tests: no key or internet needed
    tests = [
        ('{"a": 1}', {"a": 1}),
        ('```json\n{"a": 1}\n```', {"a": 1}),
        ('Sure! Here it is: {"a": 1} hope that helps', {"a": 1}),
        ('[1, 2, 3]', [1, 2, 3]),
    ]
    ok = 0
    for raw, expected in tests:
        got = _extract_json(raw)
        good = got == expected
        ok += good
        print(("PASS" if good else "FAIL"), "parse:", raw[:40].replace("\n", " "))
    try:
        _extract_json("no json here")
        print("FAIL  should have raised on text without JSON")
    except (json.JSONDecodeError, ValueError):
        ok += 1
        print("PASS  rejects text without JSON")
    print(f"\n{ok}/{len(tests) + 1} parser tests passed\n")

    # 2) real call
    if os.getenv("LLM_FAKE") == "1":
        print("LLM_FAKE=1 -> skipping the real Gemini call")
    else:
        print(f"Calling Gemini ({config.MODEL}) ...")
        try:
            answer = ask_json(
                'Classify this email into one of BL_COMPARISON, INVOICE_QUERY, GENERAL, SPAM. '
                'Email: "Please cancel invoice 5250078655 and reverse the PGI." '
                'Reply as JSON: {"category": "...", "reason": "..."}'
            )
            print("Gemini answered:", answer)
            print("\nSUCCESS: llm.py works.")
        except LLMError as e:
            print("FAILED:", e)