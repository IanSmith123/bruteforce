from bruteforce import multi_thread_request
import queue

q = queue.Queue(10)


def login(username, password) -> dict:
    """
    登录和检测登录结果的代码分别完成
    :param username:
    :param password:
    :return:
    """
    success = True
    msg = "admin:123456"

    return {
        "success": success,
        "msg": msg
    }


if __name__ == "__main__":
    result = queue.Queue()
    dic = dict()
    try:
        multi_thread_request(login, dic=dic, result=result, t=10)
    except KeyboardInterrupt:
        print(result)
