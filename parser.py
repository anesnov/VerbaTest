from ast import parse
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

# Получение всех товаров на странице
def get_products(response):
    products = []

    products_raw = response.get('products', None)

    products_scrapper = ProductScrapper()

    count = 1

    while products_raw is not None and len(products) < len(products_raw):
        for item in products_raw:

            product = products_scrapper.get_product_info(item['id']).get('products')
            desk = products_scrapper.get_product_description(item['id'])
            product[0]['description'] = desk
            product[0]['images'] = products_scrapper.get_product_images(item['id'], item['pics'])

            parsed_product = parse_wb_json(product[0])

            products.append(parsed_product)

            print(f'Обработано товаров: {count}')
            count += 1

    return products

#
def parse_wb(query):
    iterclass = PageIter(query)
    pageiter = iter(iterclass)

    writer = XSLSWriter("all", "filtered")
    try:
        while True:
            count = 1
            products = get_products(next(pageiter))
            if len(products) == 0 or products is None:
                break

            for product in products:
                if product.get("country") == "Россия" and product.get("rating") >= 4.5 and product.get("price") < 10000:
                    writer.write_item_to_ws(product, "filtered")
                else:
                    writer.write_item_to_ws(product, "all")

            print(f'Страница {count} обработана')
            count += 1
            sleep(1)
    except Exception as e:
        print(e)
        print("Преждевременная остановка парсинга")

    writer.save_to_excel("all", "wb_all.xlsx")
    writer.save_to_excel("filtered", "wb_filtered.xlsx")


parse_wb(QUERY)