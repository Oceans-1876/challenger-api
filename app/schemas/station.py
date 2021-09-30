"""Pydantic models for representing station data extracted by `challenger-workflows`.
"""
import json
from datetime import date
from typing import Dict, List, Optional

from geoalchemy2 import WKBElement
from pydantic import BaseModel, validator

from app.schemas.geojson import Point
from app.schemas.species import SpeciesID


class StationBase(BaseModel):
    name: str
    sediment_sample: Optional[str] = None
    coordinates: Point

    @validator("coordinates", pre=True)
    def to_point(cls, value: WKBElement) -> Point:
        """Convert the WKBElement receieved from SQLAlchemy to json (`Point`)."""
        return json.loads(value.data)

    location: str
    water_body: str
    sea_area: Optional[str] = None
    place: Optional[str] = None
    date: date
    fao_area: int
    gear: Optional[str] = None
    depth_fathoms: Optional[int] = None
    bottom_water_temp_c: Optional[float] = None
    bottom_water_depth_fathoms: Optional[int] = None
    specific_gravity_at_bottom: Optional[float] = None
    surface_temp_c: Optional[float] = None
    specific_gravity_at_surface: Optional[float] = None
    water_temp_c_at_depth_fathoms: Dict[str, Optional[float]]
    text: str


class StationCreate(StationBase):
    pass


class StationUpdate(StationBase):
    pass


class StationInDB(StationBase):
    species: List[SpeciesID]
    # species: SpeciesID

    class Config:
        orm_mode = True


class Station(StationInDB):
    pass
