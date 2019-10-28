PROXY_POOL_URL = 'http://127.0.0.1:5010/get/'  # 获取可用代理url
LOGIN_URL = 'http://ss.gentlecp.com:40000/user/login/?referer=/'
LOGIN_LIMIT_IP_URL = 'http://ss.gentlecp.com:40000/user/login_limit_ip/?referer=/'


MAX_ROUND = 3  # 爆破的轮数
curr_round = 0  # 当前的轮数
sleep_time = 2  # 每一轮休眠的秒数