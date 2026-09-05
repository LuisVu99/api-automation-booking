"""Generic CSV-driven API tests."""

from pathlib import Path
from typing import Any

import allure
import pytest

from endpoints.base_api import BaseApi
from utils.csv_reader import read_test_cases
from utils.request_chaining import resolve_placeholders, update_chain_context
from utils.response_verifier import verify_response


CASES = read_test_cases(Path(__file__).parents[1] / "test_data" / "csv" / "user_api_cases.csv")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("case", CASES, ids=[case["case_id"] for case in CASES])
def test_api_from_csv(base_api: BaseApi, chain_context: dict[str, object], case: dict[str, Any]) -> None:
    """Execute and verify any API scenario represented by one CSV row."""
    allure.dynamic.title(case.get("Title") or case["case_id"])
    allure.dynamic.label("test_case_id", case["case_id"])
    allure.dynamic.severity(case.get("Priority", "normal").lower())
    allure.dynamic.description(f"Role: {case.get('Role', '')}\nMethod: {case['Method']}\nURL: {case['API URL']}")

    request_path = resolve_placeholders(case["API URL"], chain_context)
    request_body = resolve_placeholders(case["Request Body"], chain_context)
    response = base_api.request(
        case["Method"],
        request_path,
        json=request_body,
        role=case.get("Role", ""),
    )
    try:
        response_payload = response.json()
    except ValueError:
        response_payload = response.text
    update_chain_context(chain_context, response_payload)
    verify_response(response, case["expected_type"], case["expected_result"])
