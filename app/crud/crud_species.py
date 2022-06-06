from app.crud.base import CRUDBase
# Species
from app.models import Species, SpeciesCommonNames, SpeciesExtra, SpeciesSynonyms
from app.schemas import (
    SpeciesCommonNamesCreate,
    SpeciesCommonNamesPagination,
    SpeciesCommonNamesUpdate,
    SpeciesCreate,
    SpeciesExtraCreate,
    SpeciesExtraSummaryPagination,
    SpeciesExtraUpdate,
    SpeciesSummaryPagination,
    SpeciesSynonymsCreate,
    SpeciesSynonymsPagination,
    SpeciesSynonymsUpdate,
    SpeciesUpdate,
)


# Species
class CRUDSpecies(
    CRUDBase[Species, SpeciesCreate, SpeciesUpdate, SpeciesSummaryPagination]
):
    pass


species = CRUDSpecies(Species)


# Species Common Names
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


# Species Extra
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


# Species Synonyms
class CRUDSpeciesSynonyms(
    CRUDBase[
        SpeciesSynonyms,
        SpeciesSynonymsCreate,
        SpeciesSynonymsUpdate,
        SpeciesSynonymsPagination,
    ]
):
    pass


species_synonyms = CRUDSpeciesSynonyms(SpeciesSynonyms)
