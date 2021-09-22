from datetime import date  # noqa
from typing import TYPE_CHECKING, Dict, List, Optional

from geoalchemy2 import WKBElement
from sqlalchemy import (
    JSON,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils.db import Geometry

if TYPE_CHECKING:
    from app.models import Species

stations_species_table = Table(
    "stations_species",
    Base.metadata,
    Column("station_id", ForeignKey("stations.name"), primary_key=True),
    Column("species_id", ForeignKey("species.id"), primary_key=True),
)


class Station(Base):
    __tablename__ = "stations"

    name: str = Column(String(length=20), primary_key=True, index=True)
    sediment_sample: Optional[str] = Column(String(length=50))
    coordinates: WKBElement = Column(
        Geometry("POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    location: str = Column(String(length=200), nullable=False)
    water_body: str = Column(String(length=200), nullable=False)
    sea_area: Optional[str] = Column(String(length=200))
    place: Optional[str] = Column(String(length=200))
    date: date = Column(Date, nullable=False)  # noqa: F811
    fao_area: int = Column(Integer, nullable=False)
    gear: Optional[str] = Column(String(length=50))
    depth_fathoms: Optional[int] = Column(Integer)
    bottom_water_temp_c: Optional[float] = Column(Float)
    bottom_water_depth_fathoms: Optional[int] = Column(Integer)
    specific_gravity_at_bottom: Optional[float] = Column(Float)
    surface_temp_c: Optional[float] = Column(Float)
    specific_gravity_at_surface: Optional[float] = Column(Float)
    water_temp_c_at_depth_fathoms: Dict[str, Optional[float]] = Column(
        JSON, nullable=False
    )
    text: str = Column(Text, nullable=False)

    species: List["Species"] = relationship(
        "Species", back_populates="stations", secondary=stations_species_table
    )
