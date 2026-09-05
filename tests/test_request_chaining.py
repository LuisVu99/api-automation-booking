# """Unit tests for request chaining."""

# from utils.request_chaining import resolve_placeholders, update_chain_context


# def test_resolves_url_placeholder_from_previous_response() -> None:
#     context: dict[str, object] = {}
#     update_chain_context(context, {"booking_id": 123})

#     assert resolve_placeholders("/booking/{booking_id}", context) == "/booking/123"


# def test_resolves_nested_values_and_preserves_native_body_types() -> None:
#     context = {"response": {"data": {"items": [{"id": 7}]}}}

#     body = resolve_placeholders({"id": "{response.data.items[0].id}"}, context)

#     assert body == {"id": 7}


# def test_resolves_multiple_placeholders_in_text() -> None:
#     context = {"booking_id": 123, "user_id": 9}

#     result = resolve_placeholders("booking/{booking_id}/user/{user_id}", context)

#     assert result == "booking/123/user/9"