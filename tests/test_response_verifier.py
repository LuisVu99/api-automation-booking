# # """Unit tests for flexible CSV response assertions."""

# # from typing import Any

# # import pytest

# # from utils.response_verifier import verify_response
# """Unit tests for flexible CSV response assertions."""

# from datetime import timedelta
# from typing import Any

# import pytest

# from utils.response_verifier import verify_response


# class FakeResponse:
# 	def __init__(
# 		self,
# 		status_code: int,
# 		payload: Any,
# 		*,
# 		content: bytes | None = None,
# 		headers: dict[str, str] | None = None,
# 		elapsed_ms: float = 100,
# 	) -> None:
# 		self.status_code = status_code
# 		self._payload = payload
# 		self.text = str(payload)
# 		self.content = content if content is not None else self.text.encode()
# 		self.headers = headers or {}
# 		self.elapsed = timedelta(milliseconds=elapsed_ms)

# 	def json(self) -> Any:
# 		return self._payload


# def test_verify_status_code() -> None:
# 	verify_response(FakeResponse(201, {}), "status_code", "200, 201")


# def test_verify_body_empty() -> None:
# 	verify_response(FakeResponse(204, None, content=b""), "verify_body_empty", "true")


# def test_verify_body_empty_rejects_non_empty_body() -> None:
# 	with pytest.raises(AssertionError, match="empty=True"):
# 		verify_response(FakeResponse(200, {"id": 1}), "verify_body_empty", "true")


# @pytest.mark.parametrize(
# 	("payload", "expected_type"),
# 	[([{"id": 1}], "array"), ({"id": 1}, "object"), (True, "boolean"), (3, "number")],
# )
# def test_verify_type(payload: Any, expected_type: str) -> None:
# 	verify_response(FakeResponse(200, payload), "verify_type", expected_type)


# def test_verify_response_time_supports_milliseconds_and_seconds() -> None:
# 	response = FakeResponse(200, {}, elapsed_ms=250)

# 	verify_response(response, "response_time", "<500ms")
# 	verify_response(response, "response_time", "<= 1s")


# def test_verify_content_type_ignores_parameters() -> None:
# 	response = FakeResponse(200, {}, headers={"Content-Type": "Application/JSON; charset=utf-8"})

# 	verify_response(response, "verify_content_type", "application/json")
# 	verify_response(response, "expected_content_type", "application/json")


# def test_verify_keys_supports_nested_paths_and_array_indexes() -> None:
# 	response = FakeResponse(200, {"data": {"items": [{"id": 7}]}})

# 	verify_response(response, "verify_keys", "data.items[0].id")


# def test_verify_values_parses_json_scalars_and_nested_paths() -> None:
# 	response = FakeResponse(
# 		200,
# 		{"data": {"status": "ACTIVE", "count": 2, "enabled": True}},
# 	)

# 	verify_response(response, "verify_values", "data.status=ACTIVE, data.count=2, data.enabled=true")


# def test_verify_values_reports_mismatch() -> None:
# 	response = FakeResponse(200, {"status": "INACTIVE"})

# 	with pytest.raises(AssertionError, match="status"):
# 		verify_response(response, "verify_values", "status=ACTIVE")


# # class FakeResponse:
# #     def __init__(self, status_code: int, payload: Any) -> None:
# #         self.status_code = status_code
# #         self._payload = payload
# #         self.text = str(payload)

# #     def json(self) -> Any:
# #         return self._payload


# # def test_verify_status_code() -> None:
# #     verify_response(FakeResponse(201, {}), "status_code", "200, 201")


# # def test_verify_keys_supports_nested_paths_and_array_indexes() -> None:
# #     response = FakeResponse(200, {"data": {"items": [{"id": 7}]}})

# #     verify_response(response, "verify_keys", "data.items[0].id")


# # def test_verify_values_parses_json_scalars_and_nested_paths() -> None:
# #     response = FakeResponse(
# #         200,
# #         {"data": {"status": "ACTIVE", "count": 2, "enabled": True}},
# #     )

# #     verify_response(response, "verify_values", "data.status=ACTIVE, data.count=2, data.enabled=true")


# # def test_verify_values_reports_mismatch() -> None:
# #     response = FakeResponse(200, {"status": "INACTIVE"})

# #     with pytest.raises(AssertionError, match="status"):
# #         verify_response(response, "verify_values", "status=ACTIVE")