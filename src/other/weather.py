import requests
from os import environ

def get_temp(lat: float, lon: float) -> int:
    return round(
        requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={environ['YR_API_KEY']}"
        ).json()["main"]["temp"] - 273.15
    )

def get_conditions(lat: float, lon: float) -> dict:
    return requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={environ['YR_API_KEY']}"
    ).json()["weather"][0]