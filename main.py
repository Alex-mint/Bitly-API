import os
import requests
import argparse

from dotenv import load_dotenv
from urllib.parse import urlparse


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт позволяет сокращать \
                                     ссылки с помощью сервиса bit.ly, а также получать \
                                     количество переходов по сокращенной ссылке.')
    parser.add_argument('url', help='После main.py введите ссылку как \
                        аргумент для сокращения или проверки')
    return parser


def shorten_link(token, url):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url, "domain": "bit.ly"}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten",
                             headers=headers, json=payload)
    response.raise_for_status()
    return response


def count_clicks(token, netloc, path):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary" \
        .format(netloc, path)
    headers = {"Authorization": f"Bearer {token}"}
    params = {"unit": "month",
              "units": "-1",
              }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response


def is_bitlink(token, netloc, path):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}{}" \
        .format(netloc, path)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = create_parser()
    args = parser.parse_args()
    url = args.url
    netloc = urlparse(url).netloc
    path = urlparse(url).path

    try:
        if is_bitlink(bitly_token, netloc, path):
            response = count_clicks(bitly_token, netloc, path)
            print(f"По вашей ссылке прошли: {response.json()['total_clicks']} раз(а)")
        else:
            response = shorten_link(bitly_token, url)
            print(f"Битлинк: {response.json()['link']}")
    except requests.exceptions.HTTPError:
        print("Введите верную ссылку")


if __name__ == "__main__":  
    main()
