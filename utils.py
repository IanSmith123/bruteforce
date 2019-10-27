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
            proxies = {
                'http': 'http://' + response.text,
                'https': 'https://' + response.text,
            }
            return proxies
    except ConnectionError:
        return None
