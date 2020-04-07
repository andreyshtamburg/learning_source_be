import pytest

from app import create_app


@pytest.fixture
def app():
    # mocker.patch('flask_sqlalchemy.SQLAlchemy.init_app', return_value=True)
    # mocker.patch('flask_sqlalchemy.SQLAlchemy.create_all', return_value=True)
    # mocker.patch()
    app = create_app()
    return app
