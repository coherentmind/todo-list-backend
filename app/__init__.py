from fastapi import FastAPI
from app.api import router
from app import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    connection = db.connect()
    db.init_db(connection)
    connection.close()