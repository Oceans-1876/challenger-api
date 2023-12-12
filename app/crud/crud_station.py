from typing import Any, Optional, cast

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Station
from app.schemas import StationCreate, StationSummaryPagination, StationUpdate
from app.utils.species import binomial_only


class CRUDStation(
    CRUDBase[Station, StationCreate, StationUpdate, StationSummaryPagination]
):
    def get(self, db: Session, id: Any) -> Optional[Station]:
        station = cast(
            Station, db.query(self.model).filter(self.model.name == id).first()
        )
        if station:
            station.species = binomial_only(station.species)
        return station


station = CRUDStation(Station)
