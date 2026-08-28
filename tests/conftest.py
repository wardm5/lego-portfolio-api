import os
import tempfile

import pytest

# Must be set before `database`/`main` are imported anywhere, so the app
# never touches the real lego_collection.db file or seeds demo data.
_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"
os.environ["SEED_DEMO_DATA"] = "false"

from fastapi.testclient import TestClient  # noqa: E402

from database import Base, engine  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def _clean_db():
    """Give every test a fresh, empty schema."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(_db_path)
    except OSError:
        pass
