import requests
from urllib.parse import urlsplit, urlparse
from dotenv import load_dotenv
import os
import sys
import argparse


def shorten_link(token, link):
    api_version = "5.131"
    url = 'https://api.vk.ru/method/utils.getShortLink'

    params = {
        "access_token": token,
        "v": api_version,
        "url": link,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    short_url = response.json()

    if 'error' in short_url:
        err = short_url['error']['error_msg']
        raise requests.exceptions.HTTPError(err)

    if 'response' not in short_url or 'short_url' not in short_url['response']:
        raise requests.exceptions.HTTPError('Response not found.')

    return short_url['response']['short_url']


def count_clicks(token, link):
    api_version = "5.131"
    url = 'https://api.vk.ru/method/utils.getLinkStats'

    key = urlsplit(link).path[1:]

    params = {
        "access_token": token,
        "v": api_version,
        "key": key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    link_statistics = response.json()

    if 'error' in link_statistics:
        err = link_statistics['error']['error_msg']
        raise requests.exceptions.HTTPError(err)

    if 'response' not in link_statistics:
        raise requests.exceptions.HTTPError('Response not found.')

    if len(link_statistics['response']['stats']) > 0:
        return link_statistics['response']['stats'][0]['views']
    else:
        return 0


def is_shorten_link(token, url):
    api_version = "5.131"
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    if domain != "vk.cc" or not parsed_url.path.strip("/"):
        return False

    key = parsed_url.path.strip("/")

    method_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": api_version,
        "key": key
    }

    response = requests.get(method_url, params=params).json()

    if "error" in response:
        error_code = response["error"].get("error_code")

        if error_code == 7:
            return True
        else:
            return False
    else:
        return True


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['VK_API_TOKEN']
    #user_input = input('Enter link: ')

    parser = argparse.ArgumentParser(description='This program changes your link to shorten it and shows you how many clicks.')
    parser.add_argument('link', help="Write link")
    args = parser.parse_args()
    if args.link:
        user_input = args.link[0]

    if is_shorten_link(token, user_input):
        try:
            clicks_count = count_clicks(token, user_input)
        except requests.exceptions.HTTPError as e:
            sys.exit(
                "Can't get clicks count for url '{}': {}".format(user_input, e)
                     )

        print(f'Your link was clicked {clicks_count} times')
    else:
        try:
            short_link = shorten_link(token, user_input)
        except requests.exceptions.HTTPError as e:
            sys.exit(
                "Can't get shorten link for url '{}': {}".format(user_input, e)
            )

        print('Shorted link: ', short_link)
