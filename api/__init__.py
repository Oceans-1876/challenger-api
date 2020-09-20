from flask import Flask

from api.db import db, init_db_command, close_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    db.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    from api import stations

    app.register_blueprint(stations.bp)

    return app
