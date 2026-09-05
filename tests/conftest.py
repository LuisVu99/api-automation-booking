"""Shared pytest fixtures."""

import pytest

from config.settings import Settings, get_settings
from endpoints.base_api import BaseApi
from endpoints.user_api import UserApi


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Return validated suite settings."""
    return get_settings()


@pytest.fixture(scope="session")
def chain_context() -> dict[str, object]:
    """Store response values shared by ordered CSV cases."""
    return {}


@pytest.fixture
def user_api(settings: Settings) -> UserApi:
    """Return a fresh user API client for test isolation."""
    api = UserApi(settings)
    yield api
    api.session.close()


@pytest.fixture
def base_api(settings: Settings) -> BaseApi:
    """Return the generic request client used by CSV-driven scenarios."""
    api = BaseApi(settings)
    yield api
    api.session.close()
