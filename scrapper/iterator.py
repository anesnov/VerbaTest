import requests
import os


# Класс-итератор для перебора всех страниц
class PageIter:

    def __init__(self, query):
        self.query = query

    def __iter__(self):
        self.proxies = os.getenv('PROXIES')
        self.page = 1
        self.url = f'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search?ab_testing=false&ab_testing=false&appType=1&curr=rub&dest=123585839&hide_dtype=11&inheritFilters=false&lang=ru&page=1&query={self.query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&uclusters=9&page={self.page}'
        auth = ''
        cookie = ''
        with open("headers/auth.txt") as f:
            auth = f.read()
        with open("headers/cookie.txt") as f:
            cookie = f.read()

        self.headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'close',
        'DNT': '1',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru/catalog/0/search.aspx?search={self.query}',
        'Cookie' : cookie,
        'authorization' : auth,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        }

        return self

    def __next__(self):
        self.page += 1
        self.url = f'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search?ab_testing=false&ab_testing=false&appType=1&curr=rub&dest=123585839&hide_dtype=11&inheritFilters=false&lang=ru&page=1&query={self.query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&uclusters=9&page={self.page}'
        response = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)
        return response.json()

    def get_page(self):
        return self.page