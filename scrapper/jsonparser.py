def parse_wb_json(product):
    # 1. Артикул
    article = product.get("id")

    # 2. Ссылка на товар
    item_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"

    # 3. Название
    name = product.get("name", "")

    # 4. Цена
    price = None
    if "sizes" in product and len(product["sizes"]) > 0:
        price = product["sizes"][0].get("price", {}).get("product")
        if price is not None:
            price = price / 100

    # 5. Описание
    desc = product.get("description").get("description")

    # 6. Изображения
    images = product.get("images", [])
    images_str = ",".join(images)

    # 7. Характеристики
    options = product.get("description", {}).get("options", [])
    country = ""
    charcs = {}

    for opt in options:
        name = opt.get("name")
        value = opt.get("value")

        if name and value:
            charcs[name] = value

        # Страна производства
        if name is "Страна производства":
            country = value

    # 8. Селлер
    seller_name = product.get("supplier", "")
    seller_id = product.get("supplierId")
    seller_url = f"https://www.wildberries.ru/seller/{seller_id}" if seller_id else ""

    # 9. Размеры
    sizes = []
    if "sizes" in product:
        sizes = [s.get("name") for s in product["sizes"]]
    sizes_str = ",".join(sizes)

    # 10. Остатки
    total_quantity = product.get("totalQuantity")

    # 11. Рейтинг
    rating = product.get("nmReviewRating") or product.get("reviewRating") or product.get("rating") or 0

    # 12. Количество отзывов
    feedbacks = product.get("nmFeedbacks") or product.get("feedbacks") or 0

    return {
        "url": item_url,
        "article": article,
        "name": name,
        "price": price,
        "description": desc,
        "images": images_str,
        "characteristics": charcs,
        "country": country,
        "seller_name": seller_name,
        "seller_url": seller_url,
        "sizes": sizes_str,
        "quantity": total_quantity,
        "rating": rating,
        "feedbacks": feedbacks
    }