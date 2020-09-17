# openweather-client - Project stack

This solution consists of two Docker containers:

* ``app``: the application itself;
* ``mongodb``: a MongoDB instance.

I'll start explaining the ``mongodb`` container.

## mongodb

I chose MongoDB because it is a document store, which fits well the needs of this solution. Using this document store, I can easily convert the JSON data which comes from the OpenWeather API and push it into the database. All documents are stored in the ``requests`` collection. The document structure is designed as follows:

```
{
    _id: Integer
    timestamp: ISODate,
    pending_city_ids: ListOfInteger,
    cities: ListOfObject
}
```

Objects in ``cities`` list are stored as follows:

```
{
    city_id: Integer,
    temperature_celsius: Float,
    humidity_percent: Float
}
```

## app

The application runs two processes:

* a Flask application that provides the API endpoints;
* a worker process that pulls data from the OpenWeather API.

I chose Flask because it is a simple microframework. It is a very popular choice for microservices like this applcation. It is easy to configure and has good integration with MongoDB using a third-party library.

To run the two processes, I used the uWSGI host, which runs the Flask app and provides a spooler capable of executing background tasks. This implementation uses a local folder that stores the enqueued messages, so it is not necessary to configure a message broker. If it was needed to scale the API and the worker separately, I would choose a more robust solution like Celery and ship it in a separate container (and ship a separate message broker as well). For this simple application, I did not want to create such a structure.

I configured the spooler to run at every 5 seconds. If there's more than one task (parallel requests), the spooler executes all tasks in the same loop. However, if it exceeds the limit of 60 cities within a minute, requests are paused.

Each task run pulls up to 20 pending cities from OpenWeather (also a limitation from their API), stores them in the request document in MongoDB, and pops the cities from the pending city IDs list in the document. If there are pending cities remaining, it enqueues a new task recursively. If some task fails (e.g., cities per minute limit is exceeded), it automatically retries in the next spooler loop.

## Remarks

If I deployed this application for large scale use, I would consider at least two more choices: using a web server like Nginx and using container orchestration like Kubernetes or Swarm.
