django-redis-sessions
=======================
Redis database backend for your sessions


[![Build Status](https://travis-ci.org/martinrusev/django-redis-sessions.svg?branch=master)](https://travis-ci.org/martinrusev/django-redis-sessions)


Installation
============

* Run `pip install django-redis-sessions` or alternatively  download the tarball and run `python setup.py install`,

For Django < 1.4 run `pip install django-redis-sessions==0.3`

* Set `redis_sessions.session` as your session engine, like so:


```
SESSION_ENGINE = 'redis_sessions.session'
```

* Optional settings:

```
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = 'password'
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1

# If you prefer domain socket connection, 
# you can just add this line instead of SESSION_REDIS_HOST and SESSION_REDIS_PORT.

SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'

# Redis Sentinel 
SESSION_REDIS_SENTINEL_LIST = [(host, port), (host, port), (host, port)]
SESSION_REDIS_SENTINEL_MASTER_ALIAS = 'sentinel-master'

# Redis Pool (Horizontal partitioning)
# Splits sessions between Redis instances based on the session key.
# You can configure the connection type for each Redis instance in the pool (host/port, unix socket, redis url). 
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1
SESSION_REDIS_RETRY_ON_TIMEOUT = False
SESSION_REDIS_POOL = [
    {
        'SESSION_REDIS_HOST': 'localhost3',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
    {
        'SESSION_REDIS_HOST': 'localhost2',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
    {
        'SESSION_REDIS_HOST': 'localhost1',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
]
```



Tests
============


```
$ pip install django nose redis
# Make sure you have redis running on localhost:6379
$ nosetests
```

# [Changelog](https://github.com/martinrusev/django-redis-sessions/blob/master/CHANGELOG.md)
