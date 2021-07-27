import mysql.connector


def connect():
    return mysql.connector.connect(
        user="user",
        password="password",
        database="main",
        host="127.0.0.1:8000",
    )
