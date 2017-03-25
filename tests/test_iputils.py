import unittest

from pylib import iputils


class TestPylibIpUtils(unittest.TestCase):

    def test_function(self):
        ''' test iputils function
        '''
        self.assertTrue(iputils.is_private_ip('192.168.1.1'))
        self.assertFalse(iputils.is_private_ip('8.8.8.8'))

        int_ip = 134744072
        self.assertEqual(iputils.ip_to_int('8.8.8.8'), int_ip)
        self.assertEqual(iputils.int_to_ip(int_ip), '8.8.8.8')

        self.assertNotEqual(iputils.ip_to_int('8.8.8.8'), int_ip+1)
