import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_db() -> SQLAlchemy:
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = db

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    open_db = g.pop("db", None)

    if open_db is not None:
        open_db.close()


def init_db():
    """Clear existing data and create new tables."""
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
