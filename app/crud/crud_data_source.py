from typing import Any, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import DataSource, Species
from app.schemas import DataSourceCreate, DataSourceUpdate


class CRUDDataSource(CRUDBase[DataSource, DataSourceCreate, DataSourceUpdate]):
    def get_species(self, db: Session, id: Any) -> List[Species]:
        return self.order_by(
            db.query(Species).filter(Species.data_source_id == id),
            order_by=["matched_canonical_full_name"],
        ).all()


data_source = CRUDDataSource(DataSource)
