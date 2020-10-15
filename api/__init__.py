import json

from flask import Flask
from sqlalchemy import func
from sqlalchemy.ext.declarative import DeclarativeMeta

from api.db import db, init_db_command


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # A SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                if (
                    field in obj.__table__.c
                    and hasattr(obj.__table__.c[field].type, "name")
                    and obj.__table__.c[field].type.name == "geometry"
                ):
                    fields[field] = json.loads(
                        db.session.scalar(func.ST_AsGeoJSON(data))
                    )
                else:
                    try:
                        json.dumps(
                            data
                        )  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
            # A json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    app.json_encoder = AlchemyEncoder

    db.init_app(app)
    app.cli.add_command(init_db_command)

    from api import stations

    app.register_blueprint(stations.bp)

    return app
