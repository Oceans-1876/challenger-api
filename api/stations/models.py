from geoalchemy2 import Geometry

from api.db import db


# STATION LINES DF
"""
station	startLine	endLine
"""

# SPECIES DF
"""
station	speciesName	offsetStart	offsetEnd
df['vernacular'] = vernacularsList
df['canonicalForm'] = canonicalFormList
df['verified'] = isKnownNameList
df['dataSource'] = dataSourceList
df['gniUUID'] = gniUUIDList
df['classificationPath'] = classificationPathList
df['classificationPathRank'] = classificationPathRankList

"""
# ENVIRONMENT DF
"""
d={'currentStation':currentStation,
   'currentDate':currentDate,
   'currentDMSCoords':currentDMSCoords,
   'currentLatDegree':currentLatDegree,
   'currentLatMinute':currentLatMinute,
   'currentLatSecond':currentLatSecond,
   'currentLatCoord':currentLatCoord,
   'currentLongDegree':currentLongDegree,
   'currentLongMinute':currentLongMinute,
   'currentLongSecond':currentLongSecond,
   'currentLongCoord':currentLongCoord,
   'currentAirTempNoon':currentAirTempNoon,
   'currentAirTempNoonDegree':currentAirTempNoonDegree,
   'currentAirTempDailyMean':currentAirTempDailyMean,
   'currentAirTempDailyMeanDegree':currentAirTempDailyMeanDegree,
   'currentWaterTempSurface':currentWaterTempSurface,
   'currentWaterTempSurfaceDegree':currentWaterTempSurfaceDegree,
   'currentWaterTempBottom':currentWaterTempBottom,
   'currentWaterTempBottomDegree':currentWaterTempBottomDegree,
   'currentWaterDensitySurface':currentWaterDensitySurface,
   'currentWaterDensitySurfaceNumber':currentWaterDensitySurfaceNumber,
   'currentWaterDensityBottom':currentWaterDensityBottom,
   'currentWaterDensityBottomNumber':currentWaterDensityBottomNumber,
   'lineNumberOfDate':lineNumberOfDate,
   'lineNumberOfLatLong':lineNumberOfLatLong,
   'lineNumberAirTempNoon':lineNumberAirTempNoon,
   'lineNumberOfAirTempDailyMean':lineNumberOfAirTempDailyMean,
   'lineNumberOfWaterTempSurface':lineNumberOfWaterTempSurface,
   'lineNumberOfWaterTempBottom':lineNumberOfWaterTempBottom,
   'lineNumberOfWaterDensitySurface':lineNumberOfWaterDensitySurface,
   'lineNumberOfWaterDensityBottom':lineNumberOfWaterDensityBottom
   }
"""

species_stations = db.Table(
    "species_stations",
    db.Column("species_id", db.Integer, db.ForeignKey("species.id"), primary_key=True),
    db.Column("station_id", db.Integer, db.ForeignKey("station.id"), primary_key=True),
    #db.Column("date", db.Date),
    db.Column("date", db.Text),
    #db.Column("count", db.Integer),
    db.Column("count", db.Text),
    db.Column("notes", db.Text),
)




class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meta = db.relationship("Meta", backref="meta", lazy=True, uselist=False)
    station = db.Column(db.String(100))
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
    station_text_start_line = db.Column(db.String(100))
    station_text_end_line = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "meta": self.meta,
            "station": self.station,
            "location_name": self.location_name,
            "location_original_text": self.location_original_text,
            "location_point": self.location_point,
            "species": self.species,
            "water_conditions": self.water_conditions,
            "air_conditions": self.air_conditions,
            "images": self.images,
        }


class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

    #pages = db.Column(db.JSON)
    pages = db.Column(db.Text)
    # TODO add more attributes


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    common_name = db.Column(db.String(100)) # 'vernaculars'
    scientific_name = db.Column(db.String(100)) # 'canonical_form'
    original_name = db.Column(db.String(100), nullable=False) # 'name_string'

    # keep it in this format because different for each species and database
    # 'classification_path'
        # 'Animalia|Bilateria|Protostomia|Ecdysozoa|Arthropoda|Crustacea'
    # 'classification_path_ranks'
        # 'Kingdom|Subkingdom|Infrakingdom|Superphylum|Phylum|Subphylum'
    # instead of below
    classification_path = db.Column(db.String(1000)) # 'classificationPath'
    classification_path_rank = db.Column(db.String(1000)) # 'classificationPathRank'

    # ask expert if we should break it down more
    #phylum = db.Column(db.String(100))
    #species_class = db.Column("class", db.String(100))
    #family = db.Column(db.String(100))

    data_source = db.Column(db.String(100)) # 'dataSource'
    gni_UUID = db.Column(db.String(1000)) # 'gniUUID'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    #date = db.Column(db.Date)
    date = db.Column(db.Text)

    # TODO add attributes


class WaterCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.relationship("Station", backref="station", lazy=True, uselist=False)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

    #date = db.Column(db.Date)
    date = db.Column(db.Text)

    water_temp_surace = db.Column(db.Float)
    water_temp_bottom = db.Column(db.Float)
    water_density_surace_60F = db.Column(db.Float)
    water_density_bottom_60F = db.Column(db.Float)


class AirCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

    #date = db.Column(db.Date)
    date = db.Column(db.Text)

    air_temp_noon = db.Column(db.Float)
    air_temp_daily_mean = db.Column(db.Float)
