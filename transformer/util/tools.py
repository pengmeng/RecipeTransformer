__author__ = 'mengpeng'
import time


def gethash(string, hashrange=0xffffffff):
    return hash(string) & hashrange


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def datastamp():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))