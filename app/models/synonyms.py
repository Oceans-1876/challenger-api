from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models import Species


class SpeciesSynonyms(Base):
    __tablename__ = "species_synonyms"

    id: str = Column(String(length=300), primary_key=True, index=True)
    scientific_name: Optional[str] = Column(String(length=300), nullable=True)
    outlink: Optional[str] = Column(String(length=300))

    species_id: str = Column(String, ForeignKey("species.id"), nullable=False)

    species: "Species" = relationship("Species", back_populates="species_synonyms")
