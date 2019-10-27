from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

success_queue = Queue()  # 存储成功爆破的密码
dict_queue = Queue()  # 存储字典队列
success_username = []

brute_count = 0
start_time = datetime.now()


def multi_thread_request(fun, thread_num: int):
    """
    多线程爆破
    :param fun:
    :param thread_num:
    :return:
    """
    global brute_count
    pool = ThreadPoolExecutor(thread_num)
    pool_queue = []
    for i in range(thread_num):
        if dict_queue.empty():
            break
        pool_queue.append(pool.submit(fun, ))
        brute_count += 1

    return pool_queue


def bruteforce(fun, thread_num=10):
    """
    直接开干
    :param fun:
    :param thread_num:
    :return:
    """
    print("{} 开始爆破，设定线程 {}".format(start_time, thread_num))
    try:
        while not dict_queue.empty():
            pool_queue = multi_thread_request(fun, thread_num=thread_num)

            # 阻塞等待，不要让线程过多
            r = [t.result() for t in pool_queue]
            if not brute_count % 10:
                print("\r爆破了 {} 次".format(brute_count), end='')


    except KeyboardInterrupt:
        print("\n用户终止程序")

    except IOError:
        print("\n网络异常，请检查代码和网络连接")

    if dict_queue.empty():
        print("\n密码全部爆破完成")

    stop_brute()


def stop_brute():
    """
    停止爆破
    :return:
    """
    print("程序运行时间{}, 运行次数 {} ".format(datetime.now() - start_time, brute_count))
    success = []
    while not success_queue.empty():
        success.append(success_queue.get())
    print(success)
    exit()
