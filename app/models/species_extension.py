from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.station import stations_species_table

if TYPE_CHECKING:
    from app.models import Species


class SpeciesExtension(Base):
    __tablename__ = "species_extension"

    id: str = Column(String(length=300), primary_key=True, index=True)
    scientific_name: Column(String(length=300), nullable=True)
    status: bool = Column(Boolean, default=False)
    unaccepted_reason: Optional[str] = Column(String(length=200))
    isBrackish: Optional[bool] = Column(Boolean, default=False)
    isExtinct: Optional[bool] = Column(Boolean, default=False)
    isFreshwater: Optional[bool] = Column(Boolean, default=False)
    isMarine: Optional[bool] = Column(Boolean, default=False)
    isTerrestrial: Optional[bool] = Column(Boolean, default=False)

    species_id: int = Column(Integer, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_extension")
