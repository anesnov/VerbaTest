import requests
import os


# Получение разных данных по товару
RANGES = [
    (0, 143, '01'),
    (144, 287, '02'),
    (288, 431, '03'),
    (432, 719, '04'),
    (720, 1007, '05'),
    (1008, 1061, '06'),
    (1062, 1115, '07'),
    (1116, 1169, '08'),
    (1170, 1313, '09'),
    (1314, 1601, '10'),
    (1602, 1655, '11'),
    (1656, 1919, '12'),
    (1920, 2045, '13'),
    (1920, 2089, '14'),
    (1920, 2089, '15'),
    (1920, 2405, '16'),
    (1920, 2837, '17')
]
class ProductScrapper:

    # Инициализация класса (запись HTTP заголовка для запросов)
    def __init__(self):

        self.proxies = os.getenv('PROXIES')

        auth = ''
        cookie = ''
        with open("headers/auth.txt") as f:
            auth = f.read()
        with open("headers/cookie.txt") as f:
            cookie = f.read()

        self.basket = 1
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

    # Получение информации со страницы товара
    def get_product_info(self, product_id):
        self.url = f'https://www.wildberries.ru/__internal/card/cards/v4/detail?appType=1&curr=rub&dest=123585839&spp=30&hide_dtype=11&ab_testing=false&lang=ru&nm={product_id}'
        self.headers['Referer'] = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'

        response = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)

        return response.json()

    # Нахождение корзины "эмпирическим путём"
    def get_basket(self, vol):
        for start, end, num in RANGES:
            if start <= vol <= end:
                return num
        return 18

    # Получение развёрнутого описания
    def get_product_description(self, product_id):
        part = product_id // 1000
        vol = product_id // 100000

        # Нахождение нужной корзины с изображениями и описанием

        # Вариант 1: через известные корзины

        basket = self.get_basket(vol)
        url = f'https://basket-{basket}.wbcontent.net/vol{vol}/part{part}/{product_id}/info/ru/card.json'
        response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
        if response.status_code == 200:
            self.basket = int(basket)
            return response.json()

        response = None
        # Вариант 2: перебором с первой

        basket = 1
        while basket <= 30:
            if basket < 10:
                host = '0' + str(basket)
            else :
                host = str(basket)
            url = f'https://basket-{host}.wbcontent.net/vol{vol}/part{part}/{product_id}/info/ru/card.json'
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)

            if response.status_code == 200:
                self.basket = basket
                return response.json()
            else:
                basket += 1

        return None

    # Формирование списка ссылок на изображения в карточке
    def get_product_images(self, product_id, pics):
        images = []

        part = product_id // 1000
        vol = product_id // 100000
        # basket = 10
        # while basket <= 30:
        #     url = f'https://basket-{basket}.wbcontent.net/vol{vol}/part{part}/{product_id}/images/big/1.webp'
        #     try:
        #         response = requests.get(url=url)
        #     except SSLError:
        #         break
        #
        #     if response.status_code == 200:
        #         break
        #     else:
        #         basket += 1

        count = 1
        if self.basket < 10:
            host = '0' + str(self.basket)
        else:
            host = str(self.basket)
        for count in range(count, pics+1):

            url = f'https://basket-{host}.wbcontent.net/vol{vol}/part{part}/{product_id}/images/big/{count}.webp'
            images.append(url)

        return images
