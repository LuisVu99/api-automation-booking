"""Utilities for reading CSV-based test data."""

import csv
import json
import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def _parse_json_object(value: str | None, field_name: str, case_id: str) -> dict[str, Any]:
    """Parse a JSON object, returning an empty object for blank or invalid input."""
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        LOGGER.warning("Ignoring invalid JSON in %s for case %s", field_name, case_id)
        return {}
    if not isinstance(parsed, dict):
        LOGGER.warning("Ignoring non-object JSON in %s for case %s", field_name, case_id)
        return {}
    return parsed


def read_test_cases(file_path: str | Path) -> list[dict[str, Any]]:
    """Read executable CSV rows and convert request JSON fields to dictionaries."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Test data file was not found: {path}")

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        cases: list[dict[str, Any]] = []
        for raw_row in reader:
            row = {(key or "").strip(): (value or "").strip() for key, value in raw_row.items()}
            if not any(row.values()) or row.get("Execute", "").lower() != "yes":
                continue
            case_id = row.get("case_id", "unnamed-case")
            row["Request Body"] = _parse_json_object(row.get("Request Body"), "Request Body", case_id)
            row["expected_type"] = row.get("expected_type", "").strip()
            row["expected_result"] = row.get("expected_result", "").strip()
            cases.append(row)
        return cases
