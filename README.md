# Aircraft Database

Проект получает информацию о странах и воздушных судах с помощью открытых API, сохраняет данные в базу данных PostgreSQL и предоставляет возможность выполнять SQL-запросы через класс `DBManager`.

## Используемые технологии

- Python 3.13
- Poetry
- PostgreSQL
- psycopg2
- requests
- flake8
- black
- isort
- mypy

## Используемые API

- Nominatim API — получение координат стран.
- OpenSky Network API — получение информации о воздушных судах.

## Возможности проекта

- получение координат выбранных стран;
- загрузка информации о странах в PostgreSQL;
- получение информации о воздушных судах;
- загрузка самолетов в базу данных;
- получение данных из БД с помощью класса `DBManager`.

## Методы класса DBManager

- `get_countries_and_aeroplanes_count()` — список стран и количество самолетов в их воздушном пространстве.
- `get_all_aeroplanes()` — список всех воздушных судов.
- `get_avg_speed()` — средняя скорость самолетов.
- `get_aeroplanes_with_higher_speed()` — самолеты со скоростью выше средней.
- `get_aeroplanes_with_keyword(keyword)` — поиск самолетов по позывному.

## Установка

```bash
poetry install
```

## Запуск проекта

```bash
poetry run python main.py
```