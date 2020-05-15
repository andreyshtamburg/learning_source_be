import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    return app
