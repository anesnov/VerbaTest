import openpyxl


# Класс записи в XLSX
class XSLSWriter:

    # Создаём указанные таблицы и добавляем к ним загловки
    def __init__(self, *args):
        self.workbooks = {}

        for table in args:
            wb = openpyxl.Workbook()
            ws = wb.active

            # Заголовки
            headers = [
                "Ссылка",
                "Артикул",
                "Название",
                "Цена",
                "Описание",
                "Изображения",
                "Характеристики",
                "Селлер",
                "Ссылка на селлера",
                "Размеры",
                "Остатки по товару",
                "Рейтинг",
                "Количество отзывов"
            ]

            ws.append(headers)

            self.workbooks[table] = {"wb": wb, "ws": ws}

    # Записываем полученную карточку в нужную таблицу
    def write_item_to_ws(self, product, table):

        # Данные
        row = [
            product.get("url", ""),
            product.get("article", ""),
            product.get("name", ""),
            product.get("price", ""),
            product.get("description", ""),
            product.get("images", ""),
            product.get("characteristics", ""),
            product.get("seller_name", ""),
            product.get("seller_url", ""),
            product.get("sizes", ""),
            product.get("quantity", ""),
            product.get("rating", ""),
            product.get("feedbacks", "")
        ]

        self.workbooks[table]['ws'].append(row)

    # Сохраняем конкретную таблицу в файл
    def save_to_excel(self, table, filename):
        self.workbooks[table]['wb'].save(filename)

