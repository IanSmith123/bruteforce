from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

success_queue = Queue()  # 存储成功爆破的密码
dict_queue = Queue()  # 存储字典队列


def multi_thread_request(fun, thread_num: int):
    """
    多线程爆破
    :param fun:
    :param thread_num:
    :return:
    """
    pool = ThreadPoolExecutor(thread_num)
    pool_queue = []
    for i in range(thread_num):
        pool_queue.append(pool.submit(fun, ))

    return pool_queue


def bruteforce(fun, thread_num: int):
    """
    直接开干
    :param fun:
    :param thread_num:
    :return:
    """
    start_time = datetime.now()
    count = 0
    print("{} 开始爆破，设定线程 {}".format(start_time, thread_num))
    try:
        while not dict_queue.empty():
            pool_queue = multi_thread_request(fun, thread_num=thread_num)

            # 阻塞等待，不要让线程过多
            count += thread_num
            r = [t.result() for t in pool_queue]

    except KeyboardInterrupt:
        print("用户停止程序，程序运行时间{}, 运行次数 {} ".format(datetime.now() - start_time, count))
        success = []
        while not success_queue.empty():
            success.append(success_queue.get())
        print(success)

