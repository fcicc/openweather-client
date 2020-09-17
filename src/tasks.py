import src.repository as repository
from src.openweather_api import OpenWeatherApi
from src.spooler import spool, prepare_spooler_args

CITIES_PER_REQUEST = 20

openweather_api = OpenWeatherApi()

@spool
def execute_request(args):
    request_id = int(args['request_id'])

    request_info = repository.get_request_pending_city_ids(request_id)
    pending_city_ids = request_info['pending_city_ids']

    if pending_city_ids:
        # queries for first n city IDs
        # if the request fails, it raises an exception so the spooler shall restart the task
        request_city_ids = pending_city_ids[0:CITIES_PER_REQUEST]
        data = openweather_api.get_cities_group(request_city_ids)

        # organizes data in a dict to ease processing
        cities_dict = {
            int(d['id']): {
                'city_id': int(d['id']),
                'temperature_celsius': float(d['main']['temp']),
                'humidity_percent': float(d['main']['humidity'])
            }
            for d in data['list']
        }

        # adds data to array
        # if a queried city does not exist, saves city ID with a message
        cities = []
        for city_id in request_city_ids:
            city = cities_dict.get(city_id)
            if city is not None:
                cities.append(city)
            else:
                cities.append({
                    'city_id': city_id,
                    'message': 'City not found.'
                })

        # pushes data to DB with remaining city ids
        remaining_city_ids = pending_city_ids[CITIES_PER_REQUEST:]
        repository.push_cities_data(request_id, cities, remaining_city_ids)

        # if there are more cities to process, enqueues a new execution
        if remaining_city_ids:
            task_args = prepare_spooler_args(request_id=request_id)
            execute_request(task_args)
