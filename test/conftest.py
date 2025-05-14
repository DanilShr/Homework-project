import pytest
from fastapi.testclient import TestClient
from homework.src.database import Base, engine, session
from homework.src.models import Recipes

from homework.src.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        recipes = Recipes(
            name="test",
            time_dish=2,
            ingredients="test",
            description="test"
        )
        engine.url = ("sqlite+aiosqlite:///")
        session.add(recipes)
        session.commit()
        yield client
