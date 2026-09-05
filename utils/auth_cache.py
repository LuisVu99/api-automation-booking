"""In-memory authentication cache shared by API clients in one test session."""

from typing import Any


class AuthCache:
    """Store tokens and cookies so authentication is performed only when needed."""

    def __init__(self) -> None:
        self._tokens: dict[str, str] = {}
        self._cookies: dict[str, str] = {}

    def get_token(self, role: str) -> str:
        return self._tokens.get(role, "")

    def set_token(self, role: str, token: str) -> None:
        self._tokens[role] = token

    def invalidate(self, role: str) -> None:
        self._tokens.pop(role, None)

    def update_cookies(self, cookies: Any) -> None:
        self._cookies.update(cookies.get_dict())

    def apply_cookies(self, session: Any) -> None:
        session.cookies.update(self._cookies)