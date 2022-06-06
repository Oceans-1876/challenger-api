from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Species


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
