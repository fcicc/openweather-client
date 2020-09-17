import requests
from src.secrets import get_secret

HOST = 'http://api.openweathermap.org/data/2.5'
REQUEST_TIMEOUT_SECONDS = 30

def get_cities_group(city_ids):
    uri = '{host}/group?id={ids}&units=metric&appid={appid}'.format(
        host=HOST,
        ids=','.join(str(i) for i in city_ids),
        appid=get_secret('openweather_appid')
    )

    response = requests.get(uri, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    return response.json()
