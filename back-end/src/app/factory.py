from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.core.db import db
from app.api import create_api_blueprint
from app.cli import create_cli_blueprint


def create_app(config_overrides=dict()) -> Flask:

    # SQLAlchemy requires references to models to initialise the database
    from app.api.checkouts.models.checkout import Checkout
    from app.api.checkouts.models.checkout_item import CheckoutItem
    from app.api.products.models.product import Product

    app = Flask(__name__)
    app.config.from_object("app.core.config")
    app.config.update(**config_overrides)

    CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    SQLAlchemy.init_app(db, app)

    app.register_blueprint(
        create_api_blueprint(
            db_session=db.session,
        )
    )
    app.register_blueprint(create_cli_blueprint())

    return app
