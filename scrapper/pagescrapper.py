import time

import requests
import os

from requests.exceptions import SSLError


class ProductScreapper:
    def __init__(self):

        self.proxies = os.getenv('PROXIES')

        auth = ''
        cookie = ''
        with open("headers/auth.txt") as f:
            auth = f.read()
        with open("headers/cookie.txt") as f:
            cookie = f.read()

        self.url = ''
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'close',
            'DNT': '1',
            'Origin': 'https://www.wildberries.ru',
            'Cookie': cookie,
            'authorization': auth,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def get_product_info(self, product_id):
        self.url = f'https://www.wildberries.ru/__internal/card/cards/v4/detail?appType=1&curr=rub&dest=123585839&spp=30&hide_dtype=11&ab_testing=false&lang=ru&nm={product_id}'
        self.headers['Referer'] = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'

        response = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)
        return response.json()

    def get_product_description(self, product_id):
        part = product_id // 1000
        vol = product_id // 100000
        basket = 10
        while basket <= 30:
            url = f'https://basket-{basket}.wbcontent.net/vol{vol}/part{part}/{product_id}/info/ru/card.json'
            basket += 1
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
            if response.status_code == 200:
                return response.json()

    def get_product_images(self, product_id):
        images = []
        pic_headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 144.0) Gecko / 20100101Firefox / 144.0',
            'Accept' : 'text / html, application / xhtml + xml, application / xml; q = 0.9, * / *;q = 0.8',
            'Accept - Language' : 'ru - RU, ru; q = 0.8, en - US; q = 0.5, en; q = 0.3',
            'Accept - Encoding' : 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Sec - GPC' : '1',
            'Connection': 'close',
            'Upgrade - Insecure - Requests' : '1',
            'Sec - Fetch - Dest' : 'document',
            'Sec - Fetch - Mode' : 'navigate',
            'Sec - Fetch - Site' : 'none',
            'Sec - Fetch - User' : '?1',
            'Priority' : 'u = 0, i'
        }

        part = product_id // 1000
        vol = product_id // 100000
        basket = 10
        while basket <= 30:
            url = f'https://basket-{basket}.wbcontent.net/vol{vol}/part{part}/{product_id}/images/big/1.webp'
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
            if response.status_code == 200:
                break
            else:
                basket += 1

        count = 1
        while True:
            url = f'https://basket-{basket}.wbcontent.net/vol{vol}/part{part}/{product_id}/images/big/{count}.webp'
            try:
                response = requests.get(url=url, headers=pic_headers) # , headers=self.headers, proxies=self.proxies

            except SSLError as e:
                print(f'URL с SSLError: {url}')
                pass

            if response.status_code == 200:
                images.append(url)
                count += 1
                time.sleep(0.1)

            elif response.status_code == 404:
                return images