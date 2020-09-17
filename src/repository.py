# here, we import just "src.database" to make DB mocking possible
import src.database as database

def get_request_process_info(request_id):
    cursor = database.mongo.db.requests.aggregate([
        {
            "$match": {
                '_id': request_id
            }
        },
        {
            "$project": {
                '_id': 0,
                'processed_cities_count': {
                    '$size': '$cities',
                },
                'total_cities_count': {
                    '$add': [
                        {'$size': '$cities'},
                        {'$size': '$pending_city_ids'}
                    ]
                }
            }
        }
    ])

    # gets the first result. Pymongo has no "aggregate_one" method, so we need to use cursor library
    try:
        result = cursor.next()
        cursor.close()
        return result
    except StopIteration: # when query has no result
        return None

def get_request_pending_city_ids(request_id):
    request = database.mongo.db.requests.find_one(
        {
            '_id': request_id
        },
        {
            '_id': 0,
            'pending_city_ids': 1
        }
    )
    return request

def get_request_cities(request_id):
    request = database.mongo.db.requests.find_one(
        {
            '_id': request_id
        },
        {
            '_id': 0,
            'cities': 1
        }
    )
    return request

def request_exists(request_id):
    request = database.mongo.db.requests.find_one(
        {
            '_id': request_id
        },
        {
            '_id': 0
        }
    )
    return request is not None

def insert_request(request_id, timestamp, pending_city_ids):
    database.mongo.db.requests.insert_one({
        '_id': request_id,
        'timestamp': timestamp,
        'pending_city_ids': pending_city_ids,
        'cities': []
    })

def push_cities_data(request_id, data, pending_city_ids):
    database.mongo.db.requests.update_one(
        {
            '_id': request_id
        },
        {
            '$push': {
                'cities': {
                    '$each': data
                }
            },
            '$set': {
                'pending_city_ids': pending_city_ids
            }
        }
    )
