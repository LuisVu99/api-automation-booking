"""Authentication endpoint client."""

from endpoints.base_api import BaseApi


class AuthApi(BaseApi):
    """Expose product authentication operations."""

    def login(self, username: str, password: str):
        """Submit credentials to the product login endpoint."""
        return self.request("POST", "/auth/login", json={"username": username, "password": password})
