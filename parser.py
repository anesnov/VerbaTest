import requests
import os

proxies = os.getenv('PROXIES')


def get_query():
    url = 'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search?ab_testing=false&ab_testing=false&appType=1&autoselectFilters=false&curr=rub&dest=123585839&hide_dtype=11&inheritFilters=false&lang=ru&query=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8&resultset=filters&spp=30&suppressSpellcheck=false&uclusters=9'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE+%D0%B8%D0%B7+%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9+%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(url=url, headers=headers, proxies=proxies)

    return response.json()