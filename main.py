import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
    headers = {"Authorization": f'Bearer {token}'}
    body = {"long_url": link}
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    headers = {"Authorization": f'Bearer {token}'}
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    url_elements = urlparse(link)
    bitlink = '{}{}'.format(url_elements.netloc, url_elements.path)
    url = url_template.format(bitlink)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    count_clicks = response.json()['total_clicks']
    return count_clicks


def is_bitlink(token, url):
    headers = {"Authorization": f'Bearer {token}'}
    url_elements = urlparse(url)
    bitlink = '{}{}'.format(url_elements.netloc, url_elements.path)
    url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    url = url_template.format(bitlink)
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="введите url")
    args = parser.parse_args()
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    if is_bitlink(token, args.url):
        try:
            return f'Количество переходов по ссылке битли: {count_clicks(token, args.url)}'
        except requests.HTTPError:
            return "Вы ввели неправильную ссылку или неверный токен."
    else:
        try:
            return shorten_link(token, args.url)
        except requests.HTTPError:
            return "Вы ввели неправильную ссылку или неверный токен."


if __name__ == '__main__':
    print(main())
