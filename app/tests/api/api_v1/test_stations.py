import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import get_settings

settings = get_settings()


def test_read_stations(client: TestClient, db: Session) -> None:
    r = client.get(f"{settings.API_V1_STR}/stations/")
    assert 200 <= r.status_code < 300
    stations = crud.species.get_multi(db)
    assert stations


@pytest.mark.parametrize("station_id", ["I"])
def test_return_200_for_existing_station(
    client: TestClient, station_id: str, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/stations/{station_id}")
    assert 200 <= r.status_code < 300


@pytest.mark.parametrize("station_id", ["Station a"])
def test_return_404_for_non_existing_station(
    client: TestClient, station_id: str, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/stations/{station_id}")
    assert r.status_code == 404
