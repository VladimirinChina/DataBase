from src.api.nominatim_api import get_country_coordinates
from src.api.opensky_api import get_aeroplanes
from src.database.db_connect import get_connection

COUNTRIES = ["Russia", "China", "Germany", "France", "Italy", "Spain", "Canada", "Japan", "India", "Brazil"]


def load_countries() -> None:
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
                (data["name"], data["min_lat"], data["max_lat"], data["min_lon"], data["max_lon"]),
            )

    conn.commit()
    conn.close()


def parse_aeroplane(state: list) -> dict:
    """
    Преобразует данные самолета из OpenSky API в словарь.
    """

    return {
        "icao24": state[0],
        "callsign": state[1].strip() if state[1] else None,
        "origin_country": state[2],
        "longitude": state[5],
        "latitude": state[6],
        "altitude": state[7],
        "velocity": state[9],
        "true_track": state[10],
    }


def load_aeroplanes() -> None:
    """
    Загружает самолеты в базу данных.
    """

    conn = get_connection()

    with conn.cursor() as cur:

        # Очистка таблицы перед новой загрузки
        cur.execute("""TRUNCATE TABLE aeroplanes RESTART IDENTITY""")

        # Получаем все страны
        cur.execute("""
            SELECT
                id,
                min_lat,
                max_lat,
                min_lon,
                max_lon
            FROM countries
        """)

        countries = cur.fetchall()

        for country in countries:

            country_id = country[0]

            min_lat = country[1]
            max_lat = country[2]
            min_lon = country[3]
            max_lon = country[4]

            states = get_aeroplanes(
                min_lat,
                max_lat,
                min_lon,
                max_lon,
            )

            if not states:
                continue

            for state in states:

                plane = parse_aeroplane(state)

                cur.execute(
                    """
                    INSERT INTO aeroplanes (
                        icao24,
                        callsign,
                        origin_country,
                        longitude,
                        latitude,
                        velocity,
                        true_track,
                        altitude,
                        country_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        plane["icao24"],
                        plane["callsign"],
                        plane["origin_country"],
                        plane["longitude"],
                        plane["latitude"],
                        plane["velocity"],
                        plane["true_track"],
                        plane["altitude"],
                        country_id,
                    ),
                )

    conn.commit()
    conn.close()
