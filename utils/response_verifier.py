"""Flexible assertions for CSV-driven API responses."""

import json
import re
from collections.abc import Mapping
from typing import Any


_PATH_TOKEN = re.compile(r"(?:^|\.)([^.\[\]]+)|\[([^\]]+)\]")
_TIME_LIMIT = re.compile(r"^(<=|>=|<|>|=)?\s*(\d+(?:\.\d+)?)\s*(ms|milliseconds?|s|seconds?)?$", re.IGNORECASE)


def verify_response(response: Any, expected_type: str, expected_result: str) -> None:
    """Verify one response according to the CSV expected type."""
    normalized_type = expected_type.strip().lower()
    if normalized_type == "status_code":
        _verify_status_code(response.status_code, expected_result)
        return
    if normalized_type == "verify_body_empty":
        _verify_body_empty(response, expected_result)
        return
    if normalized_type == "verify_type":
        _verify_type(_response_payload(response), expected_result)
        return
    if normalized_type in {"response_time", "verify_response_time"}:
        _verify_response_time(response, expected_result)
        return
    if normalized_type in {"verify_content_type", "expected_content_type"}:
        _verify_content_type(response, expected_result)
        return

    payload = _response_payload(response)
    if normalized_type == "verify_keys":
        _verify_keys(payload, expected_result)
        return
    if normalized_type == "verify_values":
        _verify_values(payload, expected_result)
        return
    raise AssertionError(
        f"Unsupported expected_type {expected_type!r}. "
        "Supported values: status_code, verify_body_empty, verify_type, "
        "response_time, verify_content_type, verify_keys, verify_values"
    )


def _response_payload(response: Any) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text


def _verify_status_code(actual: int, expected_result: str) -> None:
    expected_codes = _parse_status_codes(expected_result)
    assert actual in expected_codes, f"Expected HTTP status {expected_codes}, received {actual}"


def _parse_status_codes(expected_result: str) -> tuple[int, ...]:
    try:
        return tuple(int(value.strip()) for value in expected_result.split(",") if value.strip())
    except ValueError as error:
        raise AssertionError(f"Invalid status_code expected_result: {expected_result!r}") from error


def _verify_body_empty(response: Any, expected_result: str) -> None:
    expected_empty = _parse_expected_value(expected_result)
    if not isinstance(expected_empty, bool):
        raise AssertionError("verify_body_empty expected_result must be true or false")
    actual_empty = not response.content
    assert actual_empty == expected_empty, (
        f"Expected response body empty={expected_empty}, received empty={actual_empty}"
    )


def _verify_type(payload: Any, expected_result: str) -> None:
    expected_type = expected_result.strip().lower()
    type_names = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "bool": bool,
        "null": type(None),
    }
    if expected_type not in type_names:
        raise AssertionError(f"Unsupported response type: {expected_result!r}")
    actual_type = type_names[expected_type]
    is_expected_type = (
        isinstance(payload, actual_type)
        and not (expected_type in {"number", "integer"} and isinstance(payload, bool))
    )
    assert is_expected_type, (
        f"Expected response type {expected_type}, received {type(payload).__name__}"
    )


def _verify_response_time(response: Any, expected_result: str) -> None:
    match = _TIME_LIMIT.fullmatch(expected_result.strip())
    if not match:
        raise AssertionError(f"Invalid response_time expected_result: {expected_result!r}")
    operator = match.group(1) or "<="
    limit = float(match.group(2))
    unit = (match.group(3) or "ms").lower()
    limit_ms = limit * 1000 if unit.startswith("s") else limit
    elapsed = getattr(response, "elapsed", None)
    if elapsed is None:
        raise AssertionError("Response does not expose elapsed time")
    actual_ms = elapsed.total_seconds() * 1000
    comparisons = {
        "<": actual_ms < limit_ms,
        "<=": actual_ms <= limit_ms,
        ">": actual_ms > limit_ms,
        ">=": actual_ms >= limit_ms,
        "=": actual_ms == limit_ms,
    }
    assert comparisons[operator], (
        f"Expected response time {operator} {limit_ms:g}ms, received {actual_ms:.2f}ms"
    )


def _verify_content_type(response: Any, expected_result: str) -> None:
    expected = expected_result.strip().lower()
    actual = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    assert actual == expected, f"Expected Content-Type {expected!r}, received {actual!r}"


def _verify_keys(payload: Any, expected_result: str) -> None:
    mismatches = []
    for path in _split_items(expected_result):
        found, _ = _get_path(payload, path)
        if not found:
            mismatches.append(f"{path}: expected key to exist")
    assert not mismatches, "Response key mismatches:\n" + "\n".join(mismatches)


def _verify_values(payload: Any, expected_result: str) -> None:
    mismatches = []
    for expression in _split_items(expected_result):
        if "=" not in expression:
            mismatches.append(f"{expression}: expected format path=value")
            continue
        path, expected_text = (part.strip() for part in expression.split("=", 1))
        found, actual = _get_path(payload, path)
        expected = _parse_expected_value(expected_text)
        if not found:
            mismatches.append(f"{path}: expected {expected!r}, actual <missing>")
        elif actual != expected:
            mismatches.append(f"{path}: expected {expected!r}, actual {actual!r}")
    assert not mismatches, "Response value mismatches:\n" + "\n".join(mismatches)


def _split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_expected_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value.strip('"\' ')


def _get_path(payload: Any, path: str) -> tuple[bool, Any]:
    current = payload
    normalized_path = path.strip()
    if normalized_path.startswith("$"):
        normalized_path = normalized_path[1:].lstrip(".")
    if not normalized_path:
        return True, current

    tokens = [first or second for first, second in _PATH_TOKEN.findall(normalized_path)]
    if not tokens:
        tokens = [normalized_path]
    for token in tokens:
        if isinstance(current, Mapping) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            return False, None
    return True, current