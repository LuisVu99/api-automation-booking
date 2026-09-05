"""Reusable HTTP client foundation for API endpoint classes."""

from collections.abc import Mapping
from typing import Any

import allure
import requests

from config.settings import Settings


class BaseApi:
    """Provide consistent session, authentication, timeout, and diagnostics behavior."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        expected_status: int | tuple[int, ...] | None = None,
        role: str = "",
        _retry_auth: bool = True,
    ) -> requests.Response:
        """Send a request and attach request/response details to the Allure report."""
        url = path if path.startswith(("http://", "https://")) else f"{self.settings.api_base_url}/{path.lstrip('/')}"
        headers = self._headers_for_role(role)
        self.settings.auth_cache.apply_cookies(self.session)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=headers,
            timeout=self.settings.request_timeout_seconds,
            verify=self.settings.verify_ssl,
        )
        if response.status_code == 401 and _retry_auth and self._can_refresh_auth(role):
            self.settings.auth_cache.invalidate(role.strip().lower())
            self._login(role)
            return self.request(
                method,
                path,
                params=params,
                json=json,
                expected_status=expected_status,
                role=role,
                _retry_auth=False,
            )
        allure.attach(
            f"{method.upper()} {url}\nHeaders: {headers}\nBody: {json!r}",
            name="Request",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            response.request.body.decode() if isinstance(response.request.body, bytes) else str(response.request.body or ""),
            name="Request body (serialized)",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            response.text,
            name=f"Response {response.status_code}",
            attachment_type=allure.attachment_type.JSON,
        )
        if expected_status is not None:
            expected = (expected_status,) if isinstance(expected_status, int) else expected_status
            assert response.status_code in expected, (
                f"Expected HTTP status {expected}, received {response.status_code}: {response.text}"
            )
        return response

    def _headers_for_role(self, role: str) -> dict[str, str]:
        """Resolve per-case authentication without leaking one role into another case."""
        normalized_role = role.strip().lower()
        if not normalized_role:
            token = self.settings.api_token
        elif normalized_role == "guest":
            token = ""
        else:
            token = self.settings.auth_cache.get_token(normalized_role)
            if not token:
                token = self.settings.role_tokens.get(normalized_role, self.settings.api_token)
            if not token and self._can_refresh_auth(role):
                self._login(role)
                token = self.settings.auth_cache.get_token(normalized_role)

        headers = {"Accept": "application/json"}
        if token:
            headers["Cookie"] = f"token={token}"
        if normalized_role:
            headers["X-API-Role"] = role.strip()
        return headers

    def _can_refresh_auth(self, role: str) -> bool:
        """Refresh only named, non-guest roles with configured credentials."""
        normalized_role = role.strip().lower()
        return bool(
            normalized_role
            and normalized_role != "guest"
            and self.settings.api_username
            and self.settings.api_password
        )

    def _login(self, role: str) -> None:
        """Log in once and cache the token and cookies returned by the API."""
        normalized_role = role.strip().lower()
        response = self.session.request(
            method="POST",
            url=f"{self.settings.api_base_url}/{self.settings.auth_path.lstrip('/')}",
            json={"username": self.settings.api_username, "password": self.settings.api_password},
            headers={"Accept": "application/json"},
            timeout=self.settings.request_timeout_seconds,
            verify=self.settings.verify_ssl,
        )
        response.raise_for_status()
        self.settings.auth_cache.update_cookies(self.session.cookies)
        try:
            payload = response.json()
        except ValueError:
            payload = {}
        token = self._value_at_path(payload, self.settings.auth_token_path)
        if not isinstance(token, str) or not token:
            raise AssertionError(
                f"Authentication response does not contain a token at "
                f"{self.settings.auth_token_path!r}"
            )
        self.settings.auth_cache.set_token(normalized_role, token)

    @staticmethod
    def _value_at_path(payload: Any, path: str) -> Any:
        current = payload
        for key in path.lstrip("$").lstrip(".").split("."):
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current
