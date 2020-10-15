import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    """Clear existing data and create new tables."""
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
