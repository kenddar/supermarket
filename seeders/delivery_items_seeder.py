from sqlalchemy import text
import random
from . import products_data


def seed_delivery_items(engine):
    delivery_items_data_list = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM deliveries")
        )
        delivery_ids = [row.id for row in result.fetchall()]

    if not delivery_ids:
        print("таблица deliveries пуста")
        return

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT products.id, categories.name as category
                FROM products
                JOIN categories ON products.category_id = categories.id
            """)
        )
        products = [(row.id, row.category) for row in result.fetchall()]

    if not products:
        print("таблица products или categories пуста")
        return

    for delivery_id in delivery_ids:
        num_of_items = random.randint(1, 20)
        selected_products = random.sample(products, num_of_items)

        for product_id, category in selected_products:
            quantity = random.randint(10, 25)

            params = products_data.CATEGORY_PARAMS.get(category, {'price': (50, 500), 'expiry': (30, 180)})
            price_range = params['price']

            min_price = price_range[0] * 0.7
            max_price = price_range[1] * 0.7
            supplier_price = round(random.uniform(min_price, max_price), 2)

            delivery_items_data_list.append({
                'delivery_id': delivery_id,
                'product_id': product_id,
                'quantity': quantity,
                'supplier_price': supplier_price
            })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO delivery_items (delivery_id, product_id, quantity, supplier_price)
                VALUES (:delivery_id, :product_id, :quantity, :supplier_price)
            """),
            delivery_items_data_list
        )
        conn.commit()

    print(f"добавлено {len(delivery_items_data_list)} записей в таблицу delivery_items")
