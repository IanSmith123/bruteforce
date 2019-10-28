import argparse
import requests
import settings

from bruteforce import bruteforce, stop_brute, success_queue, dict_queue, success_username

def get_proxy():
    """
    获取代理ip
    :return:
    """
    try:
        response = requests.get(settings.PROXY_POOL_URL)
        if response.status_code == 200:
            proxy = eval(response.text)["proxy"]
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            return proxies
    except ConnectionError:
        return None

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