import click
from sqlalchemy.exc import OperationalError, IntegrityError
from flask import Blueprint
from flask.cli import with_appcontext

from app.core.db import db
from app.cli.seeds import products
from logging import Logger

logger = Logger(__name__)


def create_cli_blueprint() -> Blueprint:
    bp = Blueprint("cli", __name__)

    @bp.cli.command("create-db")
    @click.option("--drop-existing", is_flag=True)
    def create_db_command(drop_existing: bool):
        from app.api.checkouts import models
        from app.api.products import models

        if drop_existing:
            db.drop_all()
        db.create_all()

    @with_appcontext
    @bp.cli.command("seed-db")
    def seed_db_command():
        for product in products.data:
            try:
                db.session.add(product)
                db.session.commit()
            except (OperationalError, IntegrityError) as e:
                logger.error(f"\nIGNORING EXCEPTION: \n\n{e}")
                continue

    return bp
