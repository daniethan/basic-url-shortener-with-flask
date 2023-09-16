import pytest
from urlshort import create_app, Flask


@pytest.fixture
def init_app():
    app = create_app()
    yield app


@pytest.fixture
def client(init_app: Flask):
    return init_app.test_client()
