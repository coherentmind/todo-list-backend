from app import db
from typing import Optional
from mysql.connector import MySQLConnection


def get_db() -> MySQLConnection:
    connection = db.connect()
    try:
        yield connection
    finally:
        connection.close()