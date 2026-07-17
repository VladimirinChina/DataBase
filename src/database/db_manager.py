from typing import Any, cast

from src.database.db_connect import get_connection


class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(self) -> None:
        """Создает подключение к базе данных."""
        self.connection = get_connection()

    def get_countries_and_aeroplanes_count(self) -> list:
        """
        Возвращает список стран и количество самолетов
        в воздушном пространстве каждой страны.
        """

        with self.connection.cursor() as cur:

            cur.execute("""
                SELECT
                    c.name,
                    COUNT(a.id)
                FROM countries c
                LEFT JOIN aeroplanes a
                    ON c.id = a.country_id
                GROUP BY c.name
                ORDER BY c.name;
            """)

            return cast(list[Any], cur.fetchall())

    def get_all_aeroplanes(self) -> list:
        """
        Возвращает список всех самолетов.
        """

        with self.connection.cursor() as cur:

            cur.execute("""
                SELECT
                    icao24,
                    callsign,
                    origin_country,
                    velocity
                FROM aeroplanes
                ORDER BY callsign;
            """)

            return cast(list[Any], cur.fetchall())

    def get_avg_speed(self) -> float | None:
        """
        Возвращает среднюю скорость самолетов.
        """

        with self.connection.cursor() as cur:

            cur.execute("""
                SELECT AVG(velocity)
                FROM aeroplanes;
            """)

            return cast(float | None, cur.fetchone()[0])

    def get_aeroplanes_with_higher_speed(self) -> list:
        """
        Возвращает самолеты,
        скорость которых выше средней.
        """

        with self.connection.cursor() as cur:

            cur.execute("""
                SELECT
                    icao24,
                    callsign,
                    origin_country,
                    velocity
                FROM aeroplanes
                WHERE velocity >
                    (
                        SELECT AVG(velocity)
                        FROM aeroplanes
                    )
                ORDER BY velocity DESC;
            """)

            return cast(list[Any], cur.fetchall())

    def get_aeroplanes_with_keyword(self, keyword: str) -> list:
        """
        Возвращает самолеты,
        в позывном которых содержится keyword.
        """

        with self.connection.cursor() as cur:

            cur.execute(
                """
                SELECT
                    icao24,
                    callsign,
                    origin_country,
                    velocity
                FROM aeroplanes
                WHERE callsign ILIKE %s
                ORDER BY callsign;
            """,
                (f"%{keyword}%",),
            )

            return cast(list[Any], cur.fetchall())

    def close_connection(self) -> None:
        """Закрывает соединение с базой данных."""

        self.connection.close()
