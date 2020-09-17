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

To run the two processes, I used the uWSGI host, which runs the Flask app and provides a spooler capable of executing background tasks. This implementation uses a local folder that stores the enqueued messages, so it is not necessary to configure a message broker. If it was needed to scale the API and the worker separately, I would choose a more robust solution like Celery and ship it in a separate container (and ship a separate message broker as well). Nevertheless, for this application, the uWSGI spooler fits our needs.

I configured the spooler to run in at least every 20 seconds. Since OpenWeather API accepts 20 cities per request and 60 cities per minute, this configuration avoids exceeding these limitations. Obviously, I do not run tasks in parallel.

Each task run pulls 20 pending cities from OpenWeather, stores them in the request document in MongoDB, and pops the cities from the pending city IDs list in the document. If there are pending cities remaining, it enqueues a new task recursively. This approach allows me to control the request frequency by the spooler configuration, without having to code. It is also easy to unit-test: I just mock the spooler queue calls (either in API and recursive) to run the tasks synchronously.

If I deployed this application for large scale use, I would consider at least two more choices: using a web server like Nginx and using container orchestration like Kubernetes or Swarm.
