from typing import Dict
from fastapi.testclient import TestClient
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
import pytest
from app import crud, schemas
from app.core.config import get_settings

import requests

settings = get_settings()

from fastapi import FastAPI, Request


def test_read_species(client: TestClient, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/species/")
    assert 200 <= r.status_code < 300
    # created_user = r.json()
    species = crud.species.get_multi(db)
    assert species


@pytest.mark.parametrize(
    "species_id",
    [
        "136d74e4-2f2d-5387-8374-bd04ff82ea58",
        "4a24ad0c-a9c3-50e0-95bd-0f613f1a6501",
        "d548ad03-22dc-595b-8b4a-82317f094c56",
    ],
)
def test_read_species_by_id(client: TestClient, species_id: str, db: Session) -> None:
    # data = {"email": username, "password": password}
    r = client.get(f"{settings.API_V1_STR}/species/{species_id}")
    assert 200 <= r.status_code < 300
    sp = r.json()
    assert sp["id"] == species_id
