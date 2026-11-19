def test_initial_list_empty(client):
    assert client.get("/objects").json() == []

def test_create(client,payload):
    r=client.post("/objects",json=payload)
    assert r.status_code==201 and r.json()["id"]==1

def test_list_after_create(client,payload):
    client.post("/objects",json=payload)
    assert len(client.get("/objects").json())==1

def test_get_one(client,payload):
    i=client.post("/objects",json=payload).json()["id"]
    assert client.get(f"/objects/{i}").json()["name"]=="Cube"

def test_get_missing(client):
    assert client.get("/objects/999").status_code==404

def test_update(client,payload):
    i=client.post("/objects",json=payload).json()["id"]
    payload["name"]="Sphere"
    assert client.put(f"/objects/{i}",json=payload).json()["name"]=="Sphere"

def test_update_missing(client,payload):
    assert client.put("/objects/999",json=payload).status_code==404

def test_delete(client,payload):
    i=client.post("/objects",json=payload).json()["id"]
    assert client.delete(f"/objects/{i}").status_code==204
    assert client.get(f"/objects/{i}").status_code==404

def test_delete_missing(client):
    assert client.delete("/objects/999").status_code==404

def test_empty_name(client,payload):
    payload["name"]=""
    assert client.post("/objects",json=payload).status_code==422

def test_invalid_url(client,payload):
    payload["model_url"]="file:///secret"
    assert client.post("/objects",json=payload).status_code==422

def test_negative_scale(client,payload):
    payload["scale"]["x"]=-1
    assert client.post("/objects",json=payload).status_code==422

def test_missing_position(client,payload):
    del payload["position"]
    assert client.post("/objects",json=payload).status_code==422

def test_extra_field(client,payload):
    payload["admin"]=True
    assert client.post("/objects",json=payload).status_code==422

def test_sql_injection_is_data(client,payload):
    payload["name"]="'); DROP TABLE objects; --"
    assert client.post("/objects",json=payload).status_code==201
    assert len(client.get("/objects").json())==1
