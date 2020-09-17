import pytest
import requests_mock
import datetime
import src.repository as repository
from importlib import reload
from mongomock import MongoClient
from unittest.mock import patch
from src.secrets import get_secret
from tests.sample_data import sample_city_ids, sample_result

class PyMongoMock(MongoClient):
    # mocks MongoDB with an in-memory database that accepts the same queries

    def init_app(self, app):
        return super().__init__()

def mock_spool_decorator(function):
    # mocks uWSGI spooler to execute the tasks synchronously

    def wrapper(args):
        # reverts byte array encoding
        decoded_args = {}
        for name, value in args.items():
            decoded_args[name.decode('utf-8')] = value.decode('utf-8')

        # executes the task
        function(decoded_args)

    return wrapper

@pytest.fixture
def client():
    import src.database
    import src.spooler
    import src.cities

    with patch.object(src.database, 'mongo', PyMongoMock()), \
         patch.object(src.spooler, 'spool', mock_spool_decorator), \
         patch.object(src.cities, 'city_ids', sample_city_ids), \
         requests_mock.Mocker() as requests_mocker:

        # mocks OpenWeather API requests
        URI_TEMPLATE = 'http://api.openweathermap.org/data/2.5/group?id={ids}&units=metric&appid={appid}'
        appid = get_secret('openweather_appid')

        requests_mocker.get(
            URI_TEMPLATE.format(ids=','.join(str(i) for i in sample_city_ids), appid=appid),
            json=sample_result
        )

        # reloads the tasks module to update the mocked decorator
        import src.tasks
        reload(src.tasks)

        from src.wsgi import app
        with app.test_client() as client:
            yield client

def test_get_request_ok(client):
    repository.insert_request(100, datetime.datetime.utcnow(), sample_city_ids)
    repository.push_cities_data(100,
        [
            {
                'city_id': sample_result['list'][0]['id'],
                'temperature_celsius': sample_result['list'][0]['main']['temp'],
                'humidity_percent': sample_result['list'][0]['main']['humidity']
            }
        ],
        sample_city_ids[1:]
    )

    response = client.get('/requests/100')

    assert response.status_code == 200
    assert response.json == {'process_percent': (1.0 / len(sample_city_ids)) * 100.0}

def test_get_request_not_found(client):
    response = client.get('/requests/100')

    assert response.status_code == 404
    assert response.json == {'message': 'Request "100" does not exist.'}

def test_post_request_accepted(client):
    response = client.post('/requests', json={'id': 100})

    assert response.status_code == 202
    assert response.json == {'message': 'Request started successfully.'}
    assert response.headers.get('Location') == 'http://localhost/requests/100'

    # this test mocks the tasks to run synchronously, so we assert the task results as well
    process_info = repository.get_request_process_info(100)
    pending_city_ids = repository.get_request_pending_city_ids(100)
    cities = repository.get_request_cities(100)

    assert process_info == {
        'processed_cities_count': len(sample_city_ids),
        'total_cities_count': len(sample_city_ids)
    }
    assert pending_city_ids == {'pending_city_ids': []}

    expected_cities = [
        {
            'city_id': r['id'],
            'temperature_celsius': r['main']['temp'],
            'humidity_percent': r['main']['humidity']
        }
        for r in sample_result['list']
    ]
    expected_cities.insert(4, {
        'city_id': sample_city_ids[4],
        'message': 'City not found.'
    })
    assert cities == {'cities': expected_cities}

def test_post_request_missing_id(client):
    response1 = client.post('/requests', data='')
    response2 = client.post('/requests', json={})
    response3 = client.post('/requests', json={'id': "123abc"})

    for r in [response1, response2, response3]:
        assert r.status_code == 400
        assert r.json == {'message': 'Missing "id" field. It must exist and have an integer value.'}

def test_post_request_exists(client):
    repository.insert_request(100, datetime.datetime.utcnow(), sample_city_ids)

    response = client.post('/requests', json={'id': 100})

    assert response.status_code == 400
    assert response.json == {'message': 'Request "100" already exists.'}
