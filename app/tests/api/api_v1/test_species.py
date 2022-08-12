import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import get_settings

settings = get_settings()


def test_read_species(client: TestClient, db: Session) -> None:
    r = client.get(f"{settings.API_V1_STR}/species/")
    assert r.status_code == 200


@pytest.mark.parametrize(
    "species_id",
    [
        "136d74e4-2f2d-5387-8374-bd04ff82ea58",
        "4a24ad0c-a9c3-50e0-95bd-0f613f1a6501",
        "d548ad03-22dc-595b-8b4a-82317f094c56",
    ],
)
def test_return_200_for_existing_species(
    client: TestClient, species_id: str, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/species/{species_id}")
    assert 200 <= r.status_code < 300
    sp = r.json()
    assert sp["id"] == species_id
