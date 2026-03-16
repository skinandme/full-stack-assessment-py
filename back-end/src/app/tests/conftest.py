import os

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
from app.factory import create_app
from app.core.db import db


@pytest.fixture
def app() -> Flask:
    overrides = {"TESTING": True}
    if not os.environ.get("SQLALCHEMY_DATABASE_URI"):
        overrides["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app = create_app(overrides)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def session(app: Flask) -> Session:
    with app.app_context():
        yield db.session
