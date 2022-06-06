from app.crud.base import CRUDBase
from app.models import SpeciesExtra
from app.schemas import (
    SpeciesExtraCreate,
    SpeciesExtraSummaryPagination,
    SpeciesExtraUpdate,
)


class CRUDSpeciesExtra(
    CRUDBase[
        SpeciesExtra,
        SpeciesExtraCreate,
        SpeciesExtraUpdate,
        SpeciesExtraSummaryPagination,
    ]
):
    pass


species_extra = CRUDSpeciesExtra(SpeciesExtra)
