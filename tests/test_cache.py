from time import time, sleep
import unittest

from pyx.function_cache import Cache


class TestFunCache(unittest.TestCase):

    def test_cache_args_hash(self):
        ''' test hash
        '''
        c = Cache({})
        self.assertNotEqual(c.hash_args([1, 2, 3]), c.hash_args([1, 2]))
        self.assertEqual(c.hash_args([1, 2, 3]), c.hash_args([1, 2, 3]))
        self.assertEqual(c.hash_args([]), c.hash_args([]))

        kwargs0 = {'key': "val"}
        kwargs1 = {'key': "val"}
        self.assertEqual(c.hash_kwargs(kwargs0), c.hash_kwargs(kwargs1))
        kwargs0['dict'] = {1: 2}
        self.assertNotEqual(c.hash_kwargs(kwargs0), c.hash_kwargs(kwargs1))
        kwargs1['dict'] = {1: 2}
        self.assertEqual(c.hash_kwargs(kwargs0), c.hash_kwargs(kwargs1))

    def test_cache(self):
        ''' test cache
        '''

        cache = Cache({})


        @cache.cached(timeout=1)
        def f0():
            return int(time())

        target = int(time())
        self.assertEqual(target, f0())

        sleep(2)
        self.assertNotEqual(target, f0())
