from flask import Blueprint
from flask.json import jsonify

from .models import Station

bp = Blueprint("stations", __name__, url_prefix="/stations")


@bp.route("/meta")
def meta():
    return jsonify({})


@bp.route("/")
def stations():
    return jsonify(Station.query.all())
