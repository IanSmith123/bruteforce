# coding:utf-8
import requests
import captcha_recog
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


# original_url = 'http://127.0.0.1:8000/'
# url = 'http://127.0.0.1:8000/user/login_limit_captcha/?referer=/'

def login_notoken(url, username, password, session):
    '''
    无csrf的绕过图片验证码登陆
    param url：登陆页面url
    param username：登陆用户名
    param password：用户密码
    param session：返回状态码
    '''
    img = requests.get('http://ss.gentlecp.com:40000/static/images/captcha.png').content
    # img = requests.get('http://ss.gentlecp.com:40000/static/images/captcha.png').content
    a = captcha_recog.get_captcha(img)
    captcha = ''
    for i in a:
        captcha = captcha + str(i)
    From_data = {'username': username, 'password': password, 'captcha': captcha}

    response = session.post(url, data=From_data)
    # print(response.status_code)
    return response.status_code


def captcha_bypass_verify(username, password):
    '''
    绕过图片验证码登陆的验证
    param username：登陆用户名
    param password：用户密码
    return: true or false
    '''
    s = requests.Session()  # 此次登陆验证过程使用的会话
    login_notoken('http://ss.gentlecp.com:40000/user/login_limit_captcha/?referer=/blog/', username, password, s)
    response = s.get('http://ss.gentlecp.com:40000/')
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')  # 通过请求主页面查看用户名判断登陆成功与否
    res = soup.find("nobr")
    if res == None:
        # print('登录失败')
        return False
    elif res.get_text()[1:] == username:
        print(username + ' login successfully')
        return True


'''
def get_token(html):
    soup = BeautifulSoup(html,'lxml')
    res = soup.find("input",attrs={"name":"csrfmiddlewaretoken"})
    token = res["value"]
    return token

def get_first_token_cookie(url,session):
    response = session.get(url)
    #first_cookie = response.cookies.get_dict()
    #print(response.text)
    first_token = get_token(response.text)
    #print(first_token)
    #print(first_cookie)
    return first_token

def login(url,username,password,token,session):
    img = requests.get(pic_url).content

    image = Image.open(BytesIO(img))
    image.save('./captcha.png')
    a = recognize.recognize('./captcha.png')
    captcha = ''
    for i in a:
        captcha = captcha + str(i)
    From_data = {'csrfmiddlewaretoken': token,'username': username,'password': password,'captcha': captcha}

    response = session.post(url,data=From_data)
    #print(response.status_code)
    return
'''

if __name__ == '__main__':
    # requests.get(original_url)
    username = 'sml'
    password = '123456'
    captcha_bypass_verify(username, password)

    # print(get_first_token_cookie(url))

