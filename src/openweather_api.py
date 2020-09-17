import requests
from datetime import datetime
from src.secrets import get_secret

HOST = 'http://api.openweathermap.org/data/2.5'
REQUEST_TIMEOUT_SECONDS = 30
CITIES_PER_MINUTE_LIMIT = 60

class ExceededRequestsLimitException(Exception):
    def __init__(self):
        super().__init__(self, 'Exceeded requests limit within a minute.')

class OpenWeatherApi():
    def __init__(self):
        self._requests_count = 0
        self._last_counter_update = datetime.utcnow()

    def get_cities_group(self, city_ids):
        # we need to control the number of requests within a minute manually
        # because the OpenWeather API keeps returning results even when we exceed this limit
        now = datetime.utcnow()
        diff = now - self._last_counter_update
        if diff.seconds >= 60:
            self._requests_count = 0
            self._last_counter_update = now

        self._requests_count += len(city_ids)
        if self._requests_count > CITIES_PER_MINUTE_LIMIT:
            raise ExceededRequestsLimitException()

        uri = '{host}/group?id={ids}&units=metric&appid={appid}'.format(
            host=HOST,
            ids=','.join(str(i) for i in city_ids),
            appid=get_secret('openweather_appid')
        )

        response = requests.get(uri, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        return response.json()
