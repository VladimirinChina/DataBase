from src.database.db_connect import get_connection


def create_tables() -> None:

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            min_lat NUMERIC,
            max_lat NUMERIC,
            min_lon NUMERIC,
            max_lon NUMERIC
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS aeroplanes (
            id SERIAL PRIMARY KEY,

            icao24 VARCHAR(20),

            callsign VARCHAR(50),

            origin_country VARCHAR(100),

            longitude NUMERIC,

            latitude NUMERIC,

            velocity NUMERIC,

            true_track NUMERIC,

            altitude NUMERIC,

            country_id INTEGER REFERENCES countries(id)
        );
        """)

    conn.commit()
    conn.close()
