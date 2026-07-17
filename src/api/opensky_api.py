from typing import Any, cast

import requests


def get_aeroplanes(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> list:
    """
    Получает список самолетов в заданной области.
    """

    url = "https://opensky-network.org/api/states/all"

    params = {
        "lamin": min_lat,
        "lamax": max_lat,
        "lomin": min_lon,
        "lomax": max_lon,
    }

    response = requests.get(
        url=url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    return cast(list[Any], data.get("states", []))
