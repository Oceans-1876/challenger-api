import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import get_settings

settings = get_settings()


def test_read_data_sources(client: TestClient, db: Session) -> None:
    r = client.get(f"{settings.API_V1_STR}/data_source/")
    assert r.status_code == 200


# [1, 2, 3, 4] are the ID's of the data sources which should be tested in the database.
@pytest.mark.parametrize("data_source_id", [1, 2, 3, 4])
def test_return_200_for_existing_data_source(
    client: TestClient, data_source_id: int, db: Session
) -> None:
    credentials = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    print(credentials)
    auth_token = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=credentials
    )
    print(auth_token.json())
    if auth_token.status_code == 200:
        auth_headers = {"Authorization": "Bearer " + auth_token.json()["access_token"]}
    else:
        raise Exception("Bad Authentication")
    r = client.get(
        f"{settings.API_V1_STR}/data_source/{data_source_id}", headers=auth_headers
    )
    assert r.status_code == 200
    response_ = r.json()
    assert response_["id"] == data_source_id
