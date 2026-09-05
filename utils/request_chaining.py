"""Resolve values produced by previous API cases."""

import re
from collections.abc import Mapping
from typing import Any


_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")
_PATH_PART = re.compile(r"([^.\[\]]+)|\[(\d+)\]")


def resolve_placeholders(value: Any, context: Mapping[str, Any]) -> Any:
    """Replace {path.to.value} placeholders in strings and request data."""
    if isinstance(value, str):
        return _resolve_string(value, context)
    if isinstance(value, dict):
        return {key: resolve_placeholders(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_placeholders(item, context) for item in value]
    return value


def _resolve_string(value: str, context: Mapping[str, Any]) -> Any:
    matches = list(_PLACEHOLDER.finditer(value))
    if not matches:
        return value

    if len(matches) == 1 and matches[0].group(0) == value:
        return get_chained_value(context, matches[0].group(1).strip())

    result = value
    for match in matches:
        resolved = get_chained_value(context, match.group(1).strip())
        result = result.replace(match.group(0), str(resolved))
    return result


def get_chained_value(data: Any, path: str) -> Any:
    """Read a dot or array-index path from a previous response context."""
    current = data
    normalized_path = path.strip().lstrip("$").lstrip(".")
    tokens = [token or index for token, index in _PATH_PART.findall(normalized_path)]

    if not tokens:
        raise AssertionError(f"Invalid chaining path: {path!r}")

    for token in tokens:
        if isinstance(current, Mapping) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise AssertionError(f"Chaining value {path!r} was not found")
    return current


def update_chain_context(context: dict[str, Any], payload: Any) -> None:
    """Expose response fields directly and under response for later cases."""
    context["response"] = payload
    if isinstance(payload, dict):
        context.update(payload)