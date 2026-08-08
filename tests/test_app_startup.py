from fastapi.testclient import TestClient

import model
from database import SessionLocal
from main import app, seed_if_empty


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "alive" in response.json()["message"].lower()


def test_seed_if_empty_populates_demo_data_when_db_empty(client):
    seed_if_empty()

    db = SessionLocal()
    try:
        assert db.query(model.LegoSet).count() == 3
    finally:
        db.close()


def test_seed_if_empty_is_noop_when_db_already_has_data(client):
    db = SessionLocal()
    try:
        db.add(model.LegoSet(
            set_name="Custom", set_number="99999", theme="X",
            purchase_price=1.0, quantity=1, condition="New",
        ))
        db.commit()
    finally:
        db.close()

    seed_if_empty()

    db = SessionLocal()
    try:
        assert db.query(model.LegoSet).count() == 1
    finally:
        db.close()


def test_lifespan_seeds_demo_data_when_enabled(monkeypatch):
    monkeypatch.setenv("SEED_DEMO_DATA", "true")
    with TestClient(app) as c:
        sets = c.get("/sets").json()
    assert len(sets) == 3
