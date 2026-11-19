import os
import tempfile
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with tempfile.TemporaryDirectory() as d:
        os.environ["XR_DB_PATH"] = os.path.join(d, "test.db")
        from app.main import app
        import app.main as module
        module.DB_PATH = os.environ["XR_DB_PATH"]
        with TestClient(app) as c:
            yield c

@pytest.fixture
def payload():
    return {"name":"Cube", "model_url":"https://example.com/cube.glb", "position":{"x":0,"y":1,"z":2}, "rotation":{"x":0,"y":0,"z":0}, "scale":{"x":1,"y":1,"z":1}}
