from app.crud.base import CRUDBase
from app.models import SpeciesCommonNames
from app.schemas import (
    SpeciesCommonNamesCreate,
    SpeciesCommonNamesPagination,
    SpeciesCommonNamesUpdate,
)


class CRUDSpeciesCommonNames(
    CRUDBase[
        SpeciesCommonNames,
        SpeciesCommonNamesCreate,
        SpeciesCommonNamesUpdate,
        SpeciesCommonNamesPagination,
    ]
):
    pass


species_common_names = CRUDSpeciesCommonNames(SpeciesCommonNames)
