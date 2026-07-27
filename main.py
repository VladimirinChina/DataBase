from src.database.db_manager import DBManager


def main():
    db = DBManager()

    print("\nСтраны и количество самолетов:")
    print(db.get_countries_and_aeroplanes_count())

    print("\nСредняя скорость:")
    print(db.get_avg_speed())

    print("\nСамолеты с ACA:")
    print(db.get_aeroplanes_with_keyword("ACA"))

    db.close_connection()


if __name__ == "__main__":
    main()
