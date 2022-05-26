from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.station import stations_species_table

if TYPE_CHECKING:
    from app.models import DataSource, Station, SpeciesExtension


class Species(Base):
    __tablename__ = "species"

    id: str = Column(String(length=300), primary_key=True, index=True)
    record_id: str = Column(String(length=300), index=True, unique=True, nullable=False)
    current_record_id: str = Column(String(length=300), index=True)
    matched_name: str = Column(String(length=300), nullable=False)
    matched_canonical_simple_name: Optional[str] = Column(String(length=300))
    matched_canonical_full_name: Optional[str] = Column(String(length=300))
    current_name: Optional[str] = Column(String(length=300))
    current_canonical_simple_name: Optional[str] = Column(String(length=300))
    current_canonical_full_name: Optional[str] = Column(String(length=300))
    common_name: Optional[str] = Column(String(length=300))
    classification_path: Optional[str] = Column(String(length=800))
    classification_ranks: Optional[str] = Column(String(length=800))
    classification_ids: Optional[str] = Column(String(length=800))
    outlink: Optional[str] = Column(String(length=300))

    data_source_id: int = Column(Integer, ForeignKey("data_sources.id"), nullable=False)

    data_source: "DataSource" = relationship("DataSource", back_populates="species")
    stations: List["Station"] = relationship(
        "Station", back_populates="species", secondary=stations_species_table
    )
    species_extension: List["SpeciesExtension"] = relationship(
        "SpeciesExtension", back_populates="species", cascade="all, delete"
    )
