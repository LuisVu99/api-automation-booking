"""Environment-backed application settings."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field, PrivateAttr, field_validator

from utils.auth_cache import AuthCache

load_dotenv()


class Settings(BaseModel):
    """Validated runtime settings for the API test suite."""

    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com")
    api_username: str = Field(default="")
    api_password: str = Field(default="")
    api_token: str = Field(default="")
    role_tokens: dict[str, str] = Field(default_factory=dict)
    auth_path: str = Field(default="/auth/login")
    auth_token_path: str = Field(default="token")
    _auth_cache: AuthCache = PrivateAttr(default_factory=AuthCache)

    @property
    def auth_cache(self) -> AuthCache:
        """Return the in-memory cache, excluded from serialized settings."""
        return self._auth_cache
    request_timeout_seconds: float = Field(default=30.0, gt=0)
    verify_ssl: bool = True

    @field_validator("api_base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        """Remove a trailing slash to keep endpoint paths consistent."""
        return value.rstrip("/")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build and cache settings from environment variables."""
    return Settings(
        api_base_url=os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com"),
        api_username=os.getenv("API_USERNAME", ""),
        api_password=os.getenv("API_PASSWORD", ""),
        api_token=os.getenv("API_TOKEN", ""),
        auth_path=os.getenv("API_AUTH_PATH", "/auth/login"),
        auth_token_path=os.getenv("API_TOKEN_JSON_PATH", "token"),
        role_tokens={
            role: os.getenv(f"API_TOKEN_{role.upper()}", "")
            for role in ("admin", "user", "guest")
            if os.getenv(f"API_TOKEN_{role.upper()}", "")
        },
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
        verify_ssl=os.getenv("VERIFY_SSL", "true").lower() in {"1", "true", "yes"},
    )
