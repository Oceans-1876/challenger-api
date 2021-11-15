"""Pydantic models for representing station data extracted by `challenger-workflows`.
"""
import json
from datetime import date
from typing import Dict, List, Optional

from geoalchemy2 import WKBElement
from pydantic import BaseModel, Field, validator

from app.schemas.species import SpeciesSummary


class StationBase(BaseModel):
    name: str
    date: date
    coordinates: List[float] = Field(min_items=2, max_items=2)

    @validator("coordinates", pre=True)
    def to_point(cls, value: WKBElement) -> List[float]:
        """Convert the WKBElement received from SQLAlchemy to a list of long and lat."""
        return json.loads(value.data)["coordinates"]


class StationSummaryInDB(StationBase):
    class Config:
        orm_mode = True


class StationSummary(StationSummaryInDB):
    pass


class StationDetailsBase(StationBase):
    order: int
    sediment_sample: Optional[str] = None
    location: str
    water_body: str
    sea_area: Optional[str] = None
    place: Optional[str] = None
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


class StationCreate(StationDetailsBase):
    pass


class StationUpdate(StationDetailsBase):
    pass


class StationDetailsInDB(StationDetailsBase):
    species: List[SpeciesSummary]

    class Config:
        orm_mode = True


class StationDetails(StationDetailsInDB):
    pass
