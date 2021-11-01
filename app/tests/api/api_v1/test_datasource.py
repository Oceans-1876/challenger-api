from typing import Dict
from fastapi.testclient import TestClient
from fastapi import APIRouter, Depends
import pytest
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import get_settings

import requests

settings = get_settings()

from fastapi import FastAPI, Request


def test_read_datasource(client: TestClient, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/data_source/")
    assert 200 <= r.status_code < 300
    # created_user = r.json()
    data_sources = crud.species.get_multi(db)
    assert data_sources


# [1, 2, 3, 4] are the ID's of the datasources which should be tested in the database.
@pytest.mark.parametrize("data_source_id", [1, 2, 3, 4])
def test_read_datasource_by_id(
    client: TestClient, data_source_id: int, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/data_source/{data_source_id}")
    assert 200 <= r.status_code < 300
    response_ = r.json()
    assert response_["id"] == data_source_id
