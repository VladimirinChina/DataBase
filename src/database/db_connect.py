from os import getenv

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Создает и возвращает подключение к PostgreSQL."""

    return psycopg2.connect(
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
    )
