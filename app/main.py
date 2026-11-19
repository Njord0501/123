from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
import os
import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict

DB_PATH = os.environ.get("XR_DB_PATH", "xr_objects.db")

class Vector3(BaseModel):
    model_config = ConfigDict(extra="forbid")
    x: float = Field(ge=-100000, le=100000)
    y: float = Field(ge=-100000, le=100000)
    z: float = Field(ge=-100000, le=100000)

class Scale3(BaseModel):
    model_config = ConfigDict(extra="forbid")
    x: float = Field(gt=0, le=1000)
    y: float = Field(gt=0, le=1000)
    z: float = Field(gt=0, le=1000)

class ObjectInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    model_url: str = Field(min_length=1, max_length=2048, pattern=r"^https?://")
    position: Vector3
    rotation: Vector3
    scale: Scale3

class SceneObject(ObjectInput):
    id: int

@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS objects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, model_url TEXT NOT NULL, position TEXT NOT NULL, rotation TEXT NOT NULL, scale TEXT NOT NULL)")
    yield

app = FastAPI(title="XR Scene Object Management API", lifespan=lifespan)

def decode(row):
    import json
    d = dict(row)
    for key in ("position", "rotation", "scale"):
        d[key] = json.loads(d[key])
    return d

@app.get("/objects", response_model=list[SceneObject])
def list_objects():
    with connect() as db:
        return [decode(r) for r in db.execute("SELECT * FROM objects ORDER BY id").fetchall()]

@app.get("/objects/{object_id}", response_model=SceneObject)
def get_object(object_id: int):
    with connect() as db:
        row = db.execute("SELECT * FROM objects WHERE id=?", (object_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Object not found")
    return decode(row)

@app.post("/objects", response_model=SceneObject, status_code=status.HTTP_201_CREATED)
def create_object(obj: ObjectInput):
    import json
    with connect() as db:
        cur = db.execute("INSERT INTO objects (name,model_url,position,rotation,scale) VALUES (?,?,?,?,?)", (obj.name, obj.model_url, json.dumps(obj.position.model_dump()), json.dumps(obj.rotation.model_dump()), json.dumps(obj.scale.model_dump())))
        new_id = cur.lastrowid
    return get_object(new_id)

@app.put("/objects/{object_id}", response_model=SceneObject)
def update_object(object_id: int, obj: ObjectInput):
    import json
    get_object(object_id)
    with connect() as db:
        db.execute("UPDATE objects SET name=?,model_url=?,position=?,rotation=?,scale=? WHERE id=?", (obj.name,obj.model_url,json.dumps(obj.position.model_dump()),json.dumps(obj.rotation.model_dump()),json.dumps(obj.scale.model_dump()),object_id))
    return get_object(object_id)

@app.delete("/objects/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_object(object_id: int):
    with connect() as db:
        cur = db.execute("DELETE FROM objects WHERE id=?", (object_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Object not found")
