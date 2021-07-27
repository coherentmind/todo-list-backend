from fastapi import FastAPI
from app import db, routes, crud

app = FastAPI(debug=True)
app.include_router(routes.router)
