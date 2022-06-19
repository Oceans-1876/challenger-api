from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.station import stations_species_table

if TYPE_CHECKING:
    from app.models import DataSource, Station


class SpeciesExtra(Base):
    __tablename__ = "species_extra"

    id: str = Column(String(length=300), primary_key=True, index=True)
    scientific_name: Optional[str] = Column(String(length=300), nullable=True)
    status: bool = Column(Boolean, default=False)
    unaccepted_reason: Optional[str] = Column(Text)
    valid_name: Optional[str] = Column(String(length=300), nullable=False)
    lsid: Optional[str] = Column(String(length=300), nullable=True)
    isBrackish: bool = Column(Boolean, default=False)
    isExtinct: bool = Column(Boolean, default=False)
    isFreshwater: bool = Column(Boolean, default=False)
    isMarine: bool = Column(Boolean, default=False)
    isTerrestrial: bool = Column(Boolean, default=False)

    species_id: str = Column(String, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_extra")


class SpeciesCommonNames(Base):
    __tablename__ = "species_common_names"

    id: str = Column(String(length=300), primary_key=True, index=True)
    language: str = Column(String(length=300), nullable=False)
    name: str = Column(String(length=300), nullable=False)

    species_id: str = Column(String, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_common_names")


class SpeciesSynonyms(Base):
    __tablename__ = "species_synonyms"

    id: str = Column(String(length=300), primary_key=True, index=True)
    scientific_name: Optional[str] = Column(String(length=300), nullable=True)
    outlink: Optional[str] = Column(String(length=300))

    species_id: str = Column(String, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_synonyms")


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
    species_extra: List["SpeciesExtra"] = relationship(
        "SpeciesExtra", back_populates="species", cascade="all, delete"
    )

    species_synonyms: List["SpeciesSynonyms"] = relationship(
        "SpeciesSynonyms", back_populates="species", cascade="all, delete"
    )

    species_common_names: List["SpeciesCommonNames"] = relationship(
        "SpeciesCommonNames", back_populates="species", cascade="all, delete"
    )
