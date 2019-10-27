# @Author  : GentleCP
# @Email   : 574881148@qq.com
# @File    : test.py
# @Item    : PyCharm
# @Time    : 2019-10-27 20:32
# @WebSite : https://www.gentlecp.com

import requests

response = requests.get('https://www.xicidaili.com/wt/')
print(response.status_code)