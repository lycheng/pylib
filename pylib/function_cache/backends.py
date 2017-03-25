from pylib import IS_PY2

if IS_PY2:
    import cPickle as pickle
else:
    import pickle


def redis(config):
    ''' init redis cache
    '''
    return RedisCache(config)


class RedisCache(object):

    def __init__(self, config):
        host = config.get('CACHE_REDIS_HOST', '127.0.0.1')
        port = int(config.get('CACHE_REDIS_PORT', '6379'))
        passwd = config.get('CACHE_REDIS_PASSWD', '')
        db = int(config.get('CACHE_REDIS_DB', '1'))

        import redis

        self.backend = redis.StrictRedis(host=host, port=port, db=db,
                                         password=passwd)

    def set(self, key, value, timeout=None):
        value = pickle.dumps(value)
        if not timeout:
            self.backend.set(key, value)
        else:
            self.backend.setex(key, int(timeout), value)

    def get(self, key):
        val = self.backend.get(key)
        if val:
            return pickle.loads(val)

        return None
