import requests
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


def multi_thread_request(fun, dic: Queue, result: Queue, t=2):
    """

    :param fun: 登录函数
    :param dic: 字典
    :param result: 结果队列
    :param t: 线程数量
    :return: 爆破结果
    """
    pool = ThreadPoolExecutor(t)
    l = []
    for i in range(t):
        pass

    pass



