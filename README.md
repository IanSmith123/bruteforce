# bruteforce

## bruteforce.py 

封装好的多线程爆破框架，调用

```python
from bruteforce import bruteforce, success_queue, dict_queue
```

其中`success_queue`保存成功爆破的密码

`dict_queue`保存密码字典

`bruteforce`是主入口，传入登录函数即可，第二个参数是线程数量，建议不大于20

```python
bruteforce(login, thread_num=3)
```



## 二次开发说明

开发者需要自行完成针对某个登录页面的登录实现逻辑，其中绕过验证码等方式也需要自己实现，`bruteforce`只负责多线程爆破。需要实现的内容包括三个部分。

1. `dict_queue`变量，类型为`queue.Queue`，线程安全，没有设定队列长度。用于保存登录凭证，每个元素是一个打包好的凭证，每个凭证包括用户名、密码等`login`函数需要的信息
2. `success_queue`变量，类型为`queue.Queue`，线程安全，没有设定队列长度。用于保存登录成功的凭证。
3. `login`函数，实现登录逻辑，需要的凭证来自`dict_queue.get()`，如果验证某个密码成功登录，则保存密码`success_queue.put(token)`



举例

```python
import requests

from bruteforce import bruteforce, success_queue, dict_queue


def login():
    """
    登录和检测登录结果的代码针对每个网站分别完成
    login_info中保存了登录所需要的所有信息，可以是用户名密码组合，可以是单纯的密码
    :return:
    """
    login_info = dict_queue.get()
    username = login_info[0]
    password = login_info[1]

    ################################实现登录过程开始
    payload = {
        "username": username,
        "password": password
    }
    r = requests.post("https://httpbin.org/post", data=payload)
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

    username = ['admin', 'root', 'user']

    for u in username:
        for p in passwords:
            pair = (u, p)
            dict_queue.put(pair)


if __name__ == "__main__":
    get_dict()
    bruteforce(login, thread_num=3)
   
```

