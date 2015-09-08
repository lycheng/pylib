# -*- coding: utf-8 -*-

__author__ = 'lycheng'
__email__ = "lycheng997@gmail.com"
__date__ = '2015-08-31'

try:
    import cPickle as pickle
except:
    import pickle

def redis(config):
    ''' 初始化 redis cache
    '''
    return RedisCache(config)

class RedisCache(object):

    def __init__(self, config):
        host = config.get('CACHE_REDIS_HOST', '127.0.0.1')
        port = int(config.get('CACHE_REDIS_PORT', '6379'))
        passwd = config.get('CACHE_REDIS_PASSWD', '')
        db = int(config.get('CACHE_REDIS_DB', '1'))

        import redis
        self.backend = redis.StrictRedis(host=host, port=port, db=db, \
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
