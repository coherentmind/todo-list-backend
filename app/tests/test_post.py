from fastapi.param_functions import Depends
from mysql.connector.connection import MySQLConnection
from app import db, crud, schemas
from app.api import deps
from fastapi.testclient import TestClient
import app

client = TestClient(app)


def test_create_new_user(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserCreate
) -> None:
    email = "clownfest@gmail.com"
    password = "123456789"
    request = client.post("/user/", json={"email": email, "password": password})
    assert request.status_code == 200, request.content

    result = crud.user.get(db, id=request.id)
    assert result.id == request.json()["id"]
