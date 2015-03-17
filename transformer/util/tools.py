__author__ = 'mengpeng'
import time


def gethash(string, cap=0xffffffff):
    return hash(string) & cap


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def datastamp():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))