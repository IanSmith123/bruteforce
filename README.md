# bruteforce

## bruteforce.py 

多线程爆破框架，调用

```python
from bruteforce import bruteforce, success_queue, dict_queue, success_username
```

其中`success_queue`保存成功爆破的密码

`dict_queue`保存密码字典

`success_username` 保存成功的用户名

`bruteforce`是主入口，传入登录函数即可，第二个参数是线程数量，建议不大于20

```python
bruteforce(login, thread_num=3)
```



## 二次开发说明

开发者需要自行完成针对某个登录页面的登录实现逻辑，其中绕过验证码等方式也需要自己实现，`bruteforce`只负责多线程爆破。需要实现的内容包括三个部分。

1. `dict_queue`变量，类型为`queue.Queue`，线程安全，没有设定队列长度。用于保存登录凭证，每个元素是一个打包好的凭证，每个凭证包括用户名、密码等`login`函数需要的信息
2. `success_queue`变量，类型为`queue.Queue`，线程安全，没有设定队列长度。用于保存登录成功的凭证。
3. `success_username`变量，类型为`lisst`。用于保存成功爆破了的用户名
3. `login`函数，实现登录逻辑，需要的凭证来自`dict_queue.get()`，如果验证某个密码成功登录，则保存密码`success_queue.put(token)`





