# https://gist.github.com/1202066 was the original. 
# This is a souped up version that stores things in JSON as well.

import redis
import web
import ConfigParser
import json

SESSION = 'SESSION:'


class RedisStore(web.session.Store):
    """Store for saving a session in redis:
    import rediswebpy
    session = web.session.Session(app, rediswebpy.RedisStore(), initializer={'count': 0})
    """
    def __init__(self, ip='localhost', port=6379, db=0, initialFlush=False, format='Default'):
        self.format = format
        self.redis_server = redis.StrictRedis(ip, port, db)
        if initialFlush:
            """
            flushing the database is very important when you update your
            Session object initializer dictionary argument.
            E.g.
            # Before Update:
            session = web.session.Session(app,
                                          rediswebpy.RedisStore(initialFlush=True),
                                          initializer={'a':1})
            # After Update:
            session = web.session.Session(app,
                                          rediswebpy.RedisStore(initialFlush=True),
                                          initializer={'a':1, 'b':2})
            # This will cause an error if initialFlush=False since existing
            # sessions in Redis will not contain the key 'b'.
            """
            self.redis_server.flushdb()

    def __contains__(self, key):
        # test if session exists for given key
        return bool(self.redis_server.get(SESSION + key))

    def __getitem__(self, key):
        # attempt to get session data from redis store for given key
        data = self.redis_server.get(SESSION + key)
        # if the session existed for the given key
        if data:
            # update the expiration time
            self.redis_server.expire(SESSION + key,
                                     web.webapi.config.session_parameters.timeout)
            if self.format == 'json':
                return json.loads(data)
            else:
                return self.decode(data)
        else:
            raise KeyError

    def __setitem__(self, key, value):
        # set the redis value for given key to the encoded value, and reset the
        # expiration time
        if self.format == 'json':
            formattedKey = json.dumps(value)
        else:
            formattedKey = self.encode(value)
        self.redis_server.set(SESSION + key, formattedKey)
        self.redis_server.expire(SESSION + key,
                                     web.webapi.config.session_parameters.timeout)

    def __delitem__(self, key):
        self.redis_server.delete(SESSION + key)

    def cleanup(self, timeout):
        # since redis takes care of expiration for us, we don't need to do any
        # clean up
        pass
