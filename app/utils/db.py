import geoalchemy2


class Geometry(geoalchemy2.Geometry):
    """Make `geoalchemy2.Geometry` return a GeoJSON object instead of WKT."""

    as_binary = "ST_AsGeoJSON"
