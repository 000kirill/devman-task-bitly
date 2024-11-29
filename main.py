import requests
from urllib.parse import urlparse 
import os
import argparse


parser = argparse.ArgumentParser(
    description='Описание что делает программа'
)
parser.add_argument('name', help='Ваше имя')
args = parser.parse_args()
print(args.name)



def shorten_link(token, url):
    url_method = "https://api.vk.ru/method/utils.getShortLink"
    payload = {
        "access_token": token,
        "v": 5.199,
        "url": url
    }
    response = requests.get(url_method, params=payload)
    response.raise_for_status()
    response_answer = response.json()
    
    return response_answer["response"]["short_url"] if response_answer.get("response") else "Неправельная ссылка"


def count_clicks(token, url):
    parsed = urlparse(url)
    path = parsed.path
    vk_key = path.replace("/", "")
    method = "https://api.vk.ru/method/utils.getLinkStats"
    payload = {
        "access_token": token,
        "v": 5.199,
        "key": vk_key
    }

    response = requests.get(method, params=payload)
    response.raise_for_status()
    response_answer = response.json()["response"]
    
    if response_answer.get("stats"):
        return response_answer["stats"][0]["views"]
    else:
        return "Переходов по ссылке не было"
        

def get_shorten_link_value(token, url):
    parsed = urlparse(url)
    path = parsed.path
    vk_key = path.replace("/", "")
    method = "https://api.vk.ru/method/utils.getLinkStats"
    payload = {
        "access_token": token,
        "v": 5.199,
        "key": vk_key
    }

    response = requests.get(method, params=payload)
    response.raise_for_status()
    return True if response.json().get("response") else False


def main():
    parser = argparse.ArgumentParser(description='Считает клики по ссылкам')
    parser.add_argument('url', help='Введите ссылку')
    args = parser.parse_args()
    vk_api_key = "8a39e3a28a39e3a28a39e3a28b8922862788a398a39e3a2ec8fa71786ec4c8774b39233"
    # vk_api_key = os.environ['VK_API_KEY']
    if get_shorten_link_value(vk_api_key, args.url):
        print("Количество переходов по ссылке:", count_clicks(vk_api_key, args.url))
    else:
        print(shorten_link(vk_api_key, args.url))


if __name__ == "__main__":
    main()