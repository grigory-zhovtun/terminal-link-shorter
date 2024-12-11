import requests
from urllib.parse import urljoin, urlsplit, urlparse
from dotenv import load_dotenv
import os

load_dotenv()

def shorten_link(token, link):
    api_version = "5.131"
    api = 'utils.getShortLink'
    url = urljoin('https://api.vk.ru/method/', api)

    params = {
        "access_token": token,
        "v": api_version,
        "url": link,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    response_data = response.json()

    if 'error' in response_data:
        err = response_data['error']['error_msg']
        raise requests.exceptions.HTTPError(err)

    if 'response' not in response_data or 'short_url' not in response_data['response']:
        raise requests.exceptions.HTTPError('Response not found.')

    return response_data['response']['short_url']

def count_clicks(token, link):
    api_version = "5.131"
    api = 'utils.getLinkStats'
    url = urljoin('https://api.vk.ru/method/', api)

    key = urlsplit(link).path[1:] # get only path (example: https://vk.cc/aCog35 -> /aCog35 [1:] -> aCog35)

    params = {
        "access_token": token,
        "v": api_version,
        "key": key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    response_data = response.json()

    if 'error' in response_data:
        err = response_data['error']['error_msg']
        raise requests.exceptions.HTTPError(err)

    if 'response' not in response_data:
        raise requests.exceptions.HTTPError('Response not found.')

    if len(response_data['response']['stats']) > 0:
        return response_data['response']['stats'][0]['views']
    else:
        return 0

def is_shorten_link(url):
    parsed = urlparse(url)
    return parsed.netloc == 'vk.cc'

if __name__ == '__main__':

    token = os.getenv('TOKEN')
    user_input = input('Enter link: ')

    if is_shorten_link(user_input):
        try:
            clicks_count = count_clicks(token, user_input)
        except requests.exceptions.HTTPError as e:
            exit("Can't get clicks count for url '{}': {}".format(user_input, e))

        print(clicks_count)
    else:
        try:
            short_link = shorten_link(token, user_input)
        except requests.exceptions.HTTPError as e:
            exit("Can't get shorten link for url '{}': {}".format(user_input, e))

        print('Сокращенная ссылка: ', short_link)

