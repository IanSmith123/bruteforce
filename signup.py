"""
1. 批量注册用户
2. 将注册成功的用户的信息保存到本地文件
"""

from random import choice
from random import randint
import requests
import random
import string
from datetime import datetime


username_arr = []
password_arr = []


def read_file(dict_pass="password.txt"):
    """
    读取文件
    """
    global password_arr
    with open('dict/{}'.format(dict_pass)) as f:
        password_arr = [line.strip() for line in f.readlines()]


def gen_data():
    """
    生成用户数据
    """
    st = datetime.now()
    data = []
    weak_passwords = ["123456", "12345678", "admin", "11111111", "dearbook"]

    email_suffix = ["@qq.com", "@163.com", "@firefox.com", "gmail.com"]
    email_count = 0

    username_st = 201918018670001
    username_ed = 201918018671000  # 201928018680000

    for username in range(username_st, username_ed):
        tmp_username = str(username)
        tmp_email = str(email_count)+choice(email_suffix)

        # 暂时假设10个用户里有一个是弱口令
        if email_count % 100 == 0:
            tmp_password = "123456789"
        elif email_count % 10 == 0:
            tmp_password = choice(weak_passwords)
        else:
            tmp_password = gen_random_password()

        tmp_data = [tmp_username, tmp_email, tmp_password]
        email_count = email_count + 1
        # print(tmp_data)
        data.append(tmp_data)

    ed = datetime.now()
    print("[INFO] 生成数据{0}--{1}".format(st, ed))

    return data


def batch_signup():
    """
    批量注册
    """
    url = "http://127.0.0.1:8000/user/register/?referer=/"
    data = gen_data()

    for each in data:
        username = each[0]
        email = each[1]
        password = each[2]

        payload = {
            "username": username,
            "email": email,
            "password": password,
            "password_repeat": password
        }
        r = requests.post(url, data=payload)

        if r.status_code == 200:
            success_msg = "欢迎访问GentleCP的网站"
            if success_msg in r.text:
                print("[INFO] {0} signup success!".format(payload))
            else:
                print("[ERROR] 注册失败")
        else:
            print("[ERROR] 注册失败")


def gen_random_password():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


if __name__ == "__main__":
    read_file()
    gen_data()
    batch_signup()


