from app import db
from typing import Optional


def get_db():
    connection = db.connect()
    try:
        yield connection
    finally:
        connection.close()