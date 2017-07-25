import functools
import hashlib

from . import backends


class Cache(object):
    ''' use to control cache
    '''

    def __init__(self, config):
        self.config = self.init_config(config)
        self._cache = None

    def init_config(self, config):
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        config.setdefault('CACHE_DEFAULT_TIMEOUT', 300)
        config.setdefault('CACHE_KEY_PREFIX', 'pyx_cache_')
        config.setdefault('CACHE_TYPE', 'redis')

        return config

    def hash_kwargs(self, kwargs):
        '''
        '''
        hash_obj = hashlib.md5()
        keys = sorted(kwargs.keys())
        for key in keys:
            val = kwargs[key]
            if isinstance(val, dict):
                hash_val = self.hash_kwargs(val)
            else:
                hash_str = "%s:%s" % (str(key), val)
                hash_val = hashlib.md5(hash_str.encode('utf-8')).hexdigest()

            hash_val = "%s:%s" % (key, hash_val)
            hash_obj.update(hash_val.encode('utf-8'))
        return hash_obj.hexdigest()

    def hash_args(self, args):
        ''' hash args
        '''
        hash_obj = hashlib.md5()
        for item in args:
            val = "%s:%s" % (str(item), type(item))
            hash_obj.update(val.encode('utf-8'))

        return hash_obj.hexdigest()

    @property
    def cache(self):
        if not self._cache:
            cache_type = self.config['CACHE_TYPE']
            try:
                cache_backend = getattr(backends, cache_type)
                self._cache = cache_backend(self.config)
            except AttributeError:
                raise ImportError("%s is not a valid backend" % (
                                  cache_type))
        return self._cache

    def cached(self, timeout=None):
        """
        """
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                cache_key = decorated_function.\
                    make_cache_key(f, *args, **kwargs)
                ret = self.cache.get(cache_key)
                if ret:
                    return ret
                ret = f(*args, **kwargs)
                self.cache.set(cache_key, ret,
                               timeout=decorated_function.cache_timeout)
                return ret

            def make_cache_key(f, *args, **kwargs):
                f_name = f.__name__
                cache_key = "%s:%s:%s" % (f_name,
                                          self.hash_args(args),
                                          self.hash_kwargs(kwargs))
                return cache_key

            decorated_function.cache_timeout = timeout
            decorated_function.make_cache_key = make_cache_key
            return decorated_function
        return decorator
