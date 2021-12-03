from typing import Any, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Station
from app.schemas import StationCreate, StationSummaryPagination, StationUpdate


class CRUDStation(
    CRUDBase[Station, StationCreate, StationUpdate, StationSummaryPagination]
):
    def get(self, db: Session, id: Any) -> Optional[Station]:
        return db.query(self.model).filter(self.model.name == id).first()


station = CRUDStation(Station)
