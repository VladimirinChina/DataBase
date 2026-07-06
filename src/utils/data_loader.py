from src.api.nominatim_api import get_country_coordinates
from src.database.db_connect import get_connection


COUNTRIES = [
    "Russia",
    "China",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Canada",
    "Japan",
    "India",
    "Brazil"
]


def load_countries():
    """Загружает страны в базу данных."""

    conn = get_connection()

    with conn.cursor() as cur:

        for country in COUNTRIES:

            data = get_country_coordinates(country)

            cur.execute(
                """
                INSERT INTO countries (
                    name,
                    min_lat,
                    max_lat,
                    min_lon,
                    max_lon
                )
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (name) DO NOTHING
                """,
                (
                    data["name"],
                    data["min_lat"],
                    data["max_lat"],
                    data["min_lon"],
                    data["max_lon"]
                )
            )

    conn.commit()
    conn.close()
