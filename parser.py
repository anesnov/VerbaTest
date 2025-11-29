import time
from ast import parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from scrapper.iterator import PageIter
from scrapper.pagescrapper import ProductScrapper
from scrapper.jsonparser import parse_wb_json
from scrapper.xlsxwriter import XSLSWriter


QUERY = '%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8'

"""
• Ссылка на товар +
• Артикул +
• Название +
• Цена +
• Описание +
• Ссылки на изображения через запятую +
• Описание (Дубликат?)
• Все характеристики с сохранением их структуры +
• Название селлера +
• Ссылка на селлера +
• Размеры товара через запятую + 
• Остатки по товару (число) +
• Рейтинг +
• Количество отзывов +
"""

def get_parsed_product(article, pics):
    parsed_product = None
    fail_count = 5

    while parsed_product is None and fail_count > 0:
        try:
            products_scrapper = ProductScrapper()

            product = products_scrapper.get_product_info(article).get('products')
            desc = products_scrapper.get_product_description(article)
            if desc is not None:
                product[0]['description'] = desc
            product[0]['images'] = products_scrapper.get_product_images(article, pics)

            parsed_product = parse_wb_json(product[0])
            return parsed_product

        except Exception as e:
            print(e)
            print(f"Товар {article} не обработался")
            fail_count -= 1

    return parsed_product


# Получение всех товаров на странице
def get_products(response):

    products = []

    products_raw = response.get('products', None)

    count = 1

    while products_raw is not None and len(products) < len(products_raw):
        for item in products_raw:

            products.append(get_parsed_product(item.get('id'), item.get('pics')))

            print(f'Обработано товаров: {count}')
            count += 1

    return products

def get_products_concurrent(response, max_workers=10):

    products = []

    products_raw = response.get('products', None)

    count = 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_parsed_product, item.get('id'), item.get('pics')): item for item in products_raw}

        for future in as_completed(futures):
            article = futures[future]
            data = future.result()
            if data is not None:
                print(f"[OK {count}] {article}")
                count += 1
                products.append(data)
            else:
                print(f"[FAIL {count}] {article}")

    return products

#
def parse_wb(query, stopper = 100, concurrent = True):
    iterclass = PageIter(query)
    pageiter = iter(iterclass)

    writer = XSLSWriter("all", "filtered")

    count = 1

    try:
        while True and stopper > 0:

            products = get_products_concurrent(next(pageiter), 20)
            if len(products) == 0 or products is None:
                break

            for product in products:
                if product.get("country") == "Россия" and product.get("rating") >= 4.5 and product.get("price") < 10000:
                    writer.write_item_to_ws(product, "filtered")
                else:
                    writer.write_item_to_ws(product, "all")

            print(f'Страница {count} обработана')

            stopper -= 1
            count += 1

    except Exception as e:
        print(e)

    writer.save_to_excel("all", "wb_all.xlsx")
    writer.save_to_excel("filtered", "wb_filtered.xlsx")


parse_wb(QUERY)
