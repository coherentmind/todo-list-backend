import mysql.connector
from mysql.connector import MySQLConnection
import os


def connect() -> MySQLConnection:
    return mysql.connector.connect(
        user="root",
        password="12345678",
        database="main",
        host="mysql",
    )


def init_db(db: MySQLConnection) -> None:
    scripts_location = "app/db/sql"
    cursor = db.cursor()
    for i in os.listdir(scripts_location):
        with open(scripts_location + "/" + i) as file:
            cursor.execute(file.read())
