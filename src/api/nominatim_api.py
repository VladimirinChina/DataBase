from typing import Any

import requests


def get_country_coordinates(country_name: str) -> dict[str, Any]:
    """Получает координаты страны из Nominatim."""

    url = "https://nominatim.openstreetmap.org/search"

    params: dict[str, Any] = {
        "country": country_name,
        "format": "jsonv2",
        "limit": 1,
    }

    headers = {
        "User-Agent": "AircraftCoursework/1.0",
    }

    response = requests.get(
        url=url,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return {}

    bbox = data[0]["boundingbox"]

    return {
        "name": country_name,
        "min_lat": float(bbox[0]),
        "max_lat": float(bbox[1]),
        "min_lon": float(bbox[2]),
        "max_lon": float(bbox[3]),
    }
