from pickle import dumps, loads

from redis import Redis

# Instantiate the Redis client
r = Redis()


# redis_set adds an object to the Redis database
def redis_set(key, obj):
    # Check if the object is serializable
    if not isinstance(obj, str):
        # Use pickle module to serialize the
        # object into a data format that can
        # be stored onto Redis
        obj = dumps(obj)

    # Add the object to the Redis database
    r.set(key, obj)


# redis_get fetches an object from the Redis database
def redis_get(key):
    # Retrieve the object
    obj = r.get(key)

    # Try deserializing the data
    # if it is a Python object
    try:
        obj = loads(obj)
    except Exception as e:
        print(e)
