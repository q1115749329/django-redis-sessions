from redis_sessions.session import SessionStore
from redis_sessions.session import RedisServer
from redis_sessions import settings
import time
from nose.tools import eq_, assert_false
from random import randint


##  Dev
import redis
import timeit

redis_session = SessionStore()


def test_modify_and_keys():
    eq_(redis_session.modified, False)
    redis_session['test'] = 'test_me'
    eq_(redis_session.modified, True)
    eq_(redis_session['test'], 'test_me')


def test_session_load_does_not_create_record():
    session = SessionStore('someunknownkey')
    session.load()

    eq_(redis_session.exists(redis_session.session_key), False)


def test_save_and_delete():
    redis_session['key'] = 'value'
    redis_session.save()
    eq_(redis_session.exists(redis_session.session_key), True)
    redis_session.delete(redis_session.session_key)
    eq_(redis_session.exists(redis_session.session_key), False)


def test_flush():
    redis_session['key'] = 'another_value'
    redis_session.save()
    key = redis_session.session_key
    redis_session.flush()
    eq_(redis_session.exists(key), False)


def test_items():
    redis_session['item1'], redis_session['item2'] = 1, 2
    redis_session.save()
    # Python 3.*
    eq_(set(list(redis_session.items())), set([('item2', 2), ('item1', 1)]))


def test_expiry():
    redis_session.set_expiry(1)
    # Test if the expiry age is set correctly
    eq_(redis_session.get_expiry_age(), 1)
    redis_session['key'] = 'expiring_value'
    redis_session.save()
    key = redis_session.session_key
    eq_(redis_session.exists(key), True)
    time.sleep(2)
    eq_(redis_session.exists(key), False)


def test_save_and_load():
    redis_session.set_expiry(60)
    redis_session.setdefault('item_test', 8)
    redis_session.save()
    session_data = redis_session.load()
    eq_(session_data.get('item_test'), 8)


def test_with_redis_url_config():
    settings.SESSION_REDIS_URL = 'redis://localhost'

    from redis_sessions.session import SessionStore

    redis_session = SessionStore()
    server = redis_session.server

    host = server.connection_pool.connection_kwargs.get('host')
    port = server.connection_pool.connection_kwargs.get('port')
    db = server.connection_pool.connection_kwargs.get('db')

    eq_(host, 'localhost')
    eq_(port, 6379)
    eq_(db, 0)


def test_one_connection_is_used():
    session = SessionStore('session_key_1')
    session['key1'] = 'value1'
    session.save()

    redis_server = session.server
    set_client_name_1 = 'client_name_' + str(randint(1, 1000))
    redis_server.client_setname(set_client_name_1)
    client_name_1 = redis_server.client_getname()
    eq_(set_client_name_1, client_name_1)
    del session

    session = SessionStore('session_key_2')
    session['key2'] = 'value2'
    session.save()

    redis_server = session.server
    client_name_2 = redis_server.client_getname()
    eq_(client_name_1, client_name_2)


def test_redis_pool_server_select():
    servers = [
        {
            'SESSION_REDIS_HOST': 'localhost2',
            'SESSION_REDIS_PORT': 6379,
            'SESSION_REDIS_DB': 0,
            'SESSION_REDIS_PASSWORD': None,
            'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
            'SESSION_REDIS_WEIGHT': 1,
        },
        {
            'SESSION_REDIS_HOST': 'localhost1',
            'SESSION_REDIS_PORT': 6379,
            'SESSION_REDIS_DB': 0,
            'SESSION_REDIS_PASSWORD': None,
            'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
            'SESSION_REDIS_WEIGHT': 1,
        },
    ]

    keys1 = [
        'm8f0os91g40fsq8eul6tejqpp6',
        'kcffsbb5o272et1d5e6ib7gh75',
        'gqldpha87m8183vl9s8uqobcr2',
        'ukb9bg2jifrr60fstla67knjv3',
        'k3dranjfna7fv7ijpofs6l6bj2',
        'an4no833idr9jddr960r8ikai5',
        '16b9gardpcscrj5q4a4kf3c4u7',
        'etdefnorfbvfc165c5airu77p2',
        'mr778ou0sqqme21gjdiu4drtc0',
        'ctkgd8knu5hukdrdue6im28p90'
    ]

    keys2 = [
        'jgpsbmjj6030fdr3aefg37nq47',
        'prsv0trk66jc100pipm6bb78c3',
        '84ksqj2vqral7c6ped9hcnq940',
        'bv2uc3q48rm8ubipjmolgnhul0',
        '6c8oph72pfsg3db37qsefn3746',
        'tbc0sjtl2bkp5i9n2j2jiqf4r0',
        'v0on9rorn71913o3rpqhvkknc1',
        'lmsv98ns819uo2klk3s1nusqm0',
        '0foo2bkgvrlk3jt2tjbssrsc47',
        '05ure0f6r5jjlsgaimsuk4n1k2',
    ]
    rs = RedisServer('')

    for key in keys1:
        server_key, server = rs.get_server(key, servers)
        eq_(server_key, 1)

    for key in keys2:
        server_key, server = rs.get_server(key, servers)
        eq_(server_key, 0)

def test_with_unix_url_config():
    pass

    # Uncomment this in `redis.conf`:
    # 
    # unixsocket /tmp/redis.sock
    # unixsocketperm 755

    #settings.SESSION_REDIS_URL = 'unix:///tmp/redis.sock'

    #from redis_sessions.session import SessionStore

    # redis_session = SessionStore()
    # server = redis_session.server
    #
    # host = server.connection_pool.connection_kwargs.get('host')
    # port = server.connection_pool.connection_kwargs.get('port')
    # db = server.connection_pool.connection_kwargs.get('db')
    #
    # eq_(host, 'localhost')
    # eq_(port, 6379)
    # eq_(db, 0)

# def test_load():
#     redis_session.set_expiry(60)
#     redis_session['item1'], redis_session['item2'] = 1,2
#     redis_session.save()
#     session_data = redis_session.server.get(redis_session.session_key)
#     expiry, data = int(session_data[:15]), session_data[15:]
