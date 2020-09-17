# openweather-client

``openweather-client`` is a service that collects data from the OpenWeather API and stores it in a database.

## How to run

The application was developed using Docker Engine version 19.03.12 and Docker Compose version 1.26.2.

Before executing the application, it is necessary to create a file in the path ``./secrets/.openweather_appid`` (relative to the project root path). This file must be a plain text (UTF-8) containing a valid OpenWeather API ``appid`` and must not contain like breaks.

To execute the application in development mode, navigate to the project's root folder and type the following command:

```
docker-compose up -d
```

It takes a little while to download and install the required packages. If you want to follow the application logs, type:

```
docker-compose logs -f app
```

By default, the application runs on http://localhost:5000. This configuration can be changed in ``docker-compose.yml`` file.

The application watches for code changes, making it possible to edit the code without having to manually restart the app.

## Service endpoints

### GET /requests/{id:int}

Gets information about a request. It returns:

```
{
    "process_percent": {:float}
}
```

### POST /requests

Starts a new request if it does not exist. It receives the body:

```
{
    "id": {:int}
}
```

If it starts the request, the HTTP return code is ``200 OK``. If it is not possible to start the request (e.g., the request already exists), it returns ``400 BAD REQUEST``.

## Testing

To run the automated tests, start the application in development mode and type the following command:

```
docker-compose exec app sh -c "coverage run --source src -m pytest && coverage report"
```

It shall execute the tests and show a code coverage report.

## Viewing the data

The data can be queried using the following command:

```
docker-compose exec mongodb mongo
```

It will access the MongoDB shell. Then, type:

```
use openweather
db.requests.find({}).pretty()
```

## Production deployment

To deploy the application in production mode, type:

```
docker build -t openweather-client .
```

To execute the production app, it is necessary to create another file in ``./secrets`` folder: ``.mongo_root_pwd``. It should contain a user-defined password chosen before the first deployment.

Then, type:

```
docker-compose -f docker-compose.prod.yml up -d
```

It runs on ``http://locahost:5001``. It does not contain the development dependencies and test code, so it is not to run the automated tests in production mode.

## Project structure

* ``docs``: technical documentation
* ``src``: application code
* ``tests``: test code
* ``docker-compose.yml``: configuration for development environment
* ``.dockerignore``, ``Dockerfile``, ``docker-compose.prod.yml``: configuration for production environment
* ``requirements.txt`` - application dependencies
* ``requirements_dev.txt`` - further requirements for development environment
* ``uwsgi.ini`` - web server configuration

For further technical information, see ``docs/technical_information.md``.
