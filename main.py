import os
import requests
import argparse

from dotenv import load_dotenv
from urllib.parse import urlparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?')

    return parser


def shorten_link(token, url):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url, "domain": "bit.ly"}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten",
                             headers=headers, json=payload)
    response.raise_for_status()
    return response


def count_clicks(token, url):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary" \
        .format(urlparse(url).netloc, urlparse(url).path)
    headers = {"Authorization": f"Bearer {token}"}
    params = {"unit": "month",
              "units": "-1",
              }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response


def is_bitlink(token, url):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}{}" \
        .format(urlparse(url).netloc, urlparse(url).path)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = createParser()
    namespace = parser.parse_args()
    url = namespace.url

    try:
        if is_bitlink(bitly_token, url):
            response = count_clicks(bitly_token, url)
            print(f"По вашей ссылке прошли: {response.json()['total_clicks']} раз(а)")
        else:
            response = shorten_link(bitly_token, url)
            print(f"Битлинк: {response.json()['link']}")
    except requests.exceptions.HTTPError:
        print("Введите верную ссылку")


if __name__ == "__main__":  
    main()
