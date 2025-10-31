import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_database(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path, None, None]:
    """Provide an isolated SQLite database file for tests."""
    data_dir = tmp_path_factory.mktemp("data")
    db_path = data_dir / "test_grocery.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ.setdefault("ALLOWED_ORIGINS", "http://testserver")
    yield db_path
    if db_path.exists():
        db_path.unlink()


@pytest.fixture(scope="session")
def client(test_database: Path) -> Generator[TestClient, None, None]:
    """Create a TestClient with the isolated database."""
    from main import app

    with TestClient(app) as test_client:
        yield test_client
