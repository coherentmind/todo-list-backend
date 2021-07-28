from fastapi import FastAPI
from app.api import router
from app import db

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    connection = db.connect()
    db.init_db(connection)
    connection.close()