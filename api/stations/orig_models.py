from geoalchemy2 import Geometry

from api.db import db


species_stations = db.Table(
    "species_stations",
    db.Column("species_id", db.Integer, db.ForeignKey("species.id"), primary_key=True),
    db.Column("station_id", db.Integer, db.ForeignKey("station.id"), primary_key=True),
    db.Column("date", db.Date),
    db.Column("count", db.Integer),
    db.Column("notes", db.Text),
)


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meta = db.relationship("Meta", backref="meta", lazy=True, uselist=False)
    station = db.Column(db.String(10))
    location_name = db.Column(db.String(100))
    location_original_text = db.Column(db.String(30))
    location_point = db.Column(Geometry("POINT"))
    species = db.relationship(
        "Species",
        secondary=species_stations,
        lazy="subquery",
        backref=db.backref("stations", lazy=True),
    )
    water_conditions = db.relationship("WaterCondition", backref="station", lazy=True)
    air_conditions = db.relationship("AirCondition", backref="station", lazy=True)
    images = db.relationship("Image", backref="station", lazy=True)


class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    pages = db.Column(db.JSON)
    # TODO add more attributes


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phylum = db.Column(db.String(100))
    species_class = db.Column("class", db.String(100))
    family = db.Column(db.String(100))
    common_name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    original_name = db.Column(db.String(100), nullable=False)
    # TODO add attributes


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    date = db.Column(db.Date)
    # TODO add attributes


class WaterCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    date = db.Column(db.Date)
    # TODO add attributes


class AirCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    date = db.Column(db.Date)
    # TODO add attributes
