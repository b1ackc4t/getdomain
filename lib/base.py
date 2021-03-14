"""
存放基本的通用公共函数
"""
import time
import asyncio

G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white


def info(msg):
    print(G + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "-[INFO]: " + W + msg)



