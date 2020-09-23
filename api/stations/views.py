from flask import Blueprint
from flask.json import jsonify

from .models import Station

bp = Blueprint("stations", __name__, url_prefix="/stations")


@bp.route("/meta")
def meta():
    return jsonify({})


@bp.route("/<int:practice_id>")
def stations(practice_id):
    return jsonify(Station.query.get(practice_id).serialize())
