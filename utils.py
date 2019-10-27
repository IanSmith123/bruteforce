import requests
import settings


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

get_proxy()