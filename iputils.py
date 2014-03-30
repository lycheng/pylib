#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

__author__ = 'lycheng'
__email__ = "lycheng997@gmail.com"
__date__ = '2014-01-23'

import struct
import socket
import fcntl

def ip_to_int(ip):
    return struct.unpack("!I",socket.inet_aton(ip))[0]


def int_to_ip(num):
    return socket.inet_ntoa(struct.pack("!I", num))


def is_private_ip(ip):
    ip = ip_to_int(ip)

    if ip_to_int('10.0.0.0') <= ip <= ip_to_int('10.255.255.255'):
        return True
    if ip_to_int('172.16.0.0') <= ip <= ip_to_int('172.31.255.255'):
        return True
    if ip_to_int('192.168.0.0') <= ip <= ip_to_int('192.168.255.255'):
        return True
    return False

def device_to_ip(device):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
            0X8915, struct.pack('256s', device[:15]))[20:24])
    except:
        return None



if __name__ == "__main__":
    # print is_private_ip('10.0.0.0')
    # print is_private_ip('10.255.255.255')
    # print is_private_ip('8.8.8.8')
    # print is_private_ip('172.31.255.254')
    print device_to_ip('lo')
