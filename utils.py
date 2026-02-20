import requests
from fastapi import HTTPException


def validate_artwork(external_id: str) -> dict | None:
    """
    Перевіряє, чи існує artwork за ID.
    Повертає базову інформацію про твір, якщо існує, інакше None.
    """
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    try:
        response = requests.get(url, timeout=6)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"]:
                return data["data"]
            return None
        elif response.status_code == 404:
            return None
        else:
            return None
    except requests.RequestException:
        return None


def get_artwork_validation_or_400(external_id: str) -> dict:
    """
    Використовується в ендпоінтах: або повертає дані, або кидає 400.
    """
    artwork = validate_artwork(external_id)
    if not artwork:
        raise HTTPException(
            status_code=400,
            detail=f"Artwork з ID {external_id} не знайдено в Art Institute of Chicago API"
        )
    return artwork
