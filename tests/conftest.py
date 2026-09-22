"""Shared pytest fixtures."""

import json
from pathlib import Path
import tempfile
from collections.abc import Iterator

import pytest

from config.settings import Settings, get_settings
from endpoints.base_api import BaseApi
from endpoints.user_api import UserApi

@pytest.fixture(scope="session")
def settings() -> Settings:
    """Return validated suite settings."""
    return get_settings()


def pytest_configure(config: pytest.Config) -> None:
    """Master node executes this before workers are spawned."""
    # Chỉ chạy trên Master process (hoặc khi chạy đơn luồng không có xdist)
    if not hasattr(config, "workerinput"):
        # 1. Tạo thư mục tạm ephemeral duy nhất cho lượt chạy này
        token_file = Path(tempfile.mkdtemp(prefix="auth_session-")) / "tokens.json"

        # 2. Gọi API Login lấy Token (Chỉ chạy 1 lần duy nhất)
        tokens = _perform_master_login(config)

        # 3. Ghi token vào tmp file
        token_file.write_text(json.dumps(tokens), encoding="utf-8")

        # 4. Lưu đường dẫn tmp file vào stash để chuyển cho worker
        config.stash["shared_token_file"] = str(token_file)


def pytest_configure_node(node: pytest.Item) -> None:
    """Pass the shared token file path from Master to each xdist Worker."""
    node.workerinput["shared_token_file"] = node.config.stash["shared_token_file"]


def _perform_master_login(config: pytest.Config) -> dict[str, str]:
    """Internal helper for the master node to acquire configured tokens."""
    settings = get_settings()
    api = BaseApi(settings)
    try:
        return {"admin": api.login("admin")}
    finally:
        api.session.close()

@pytest.fixture(scope="session")
def auth_tokens(request: pytest.FixtureRequest) -> dict[str, str]:
    """Session fixture to supply workers with pre-fetched tokens."""
    # Trường hợp chạy với pytest-xdist
    if hasattr(request.config, "workerinput"):
        token_file = Path(request.config.workerinput["shared_token_file"])
    else:
        # Trường hợp chạy đơn luồng (no xdist)
        token_file = Path(request.config.stash["shared_token_file"])

    if not token_file.exists():
        raise FileNotFoundError(f"Shared token file not found at {token_file}")

    return json.loads(token_file.read_text(encoding="utf-8"))

@pytest.fixture(scope="session")
def chain_context() -> dict[str, object]:
    """Store response values shared by ordered CSV cases."""
    return {}


@pytest.fixture
def user_api(settings: Settings) -> Iterator[UserApi]:
    """Return a fresh user API client for test isolation."""
    api = UserApi(settings)
    yield api
    api.session.close()


@pytest.fixture
def base_api(settings: Settings) -> Iterator[BaseApi]:
    """Return the generic request client used by CSV-driven scenarios."""
    api = BaseApi(settings)
    yield api
    api.session.close()
