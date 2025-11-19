from sqlalchemy import text
import random


def seed_transfer_items(engine):
    transfer_items_data_list = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM transfers")
        )
        transfer_ids = [row.id for row in result.fetchall()]

    if not transfer_ids:
        print("таблица transfers пуста")
        return

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM products")
        )
        product_ids = [row.id for row in result.fetchall()]

    if not product_ids:
        print("таблица products пуста")
        return

    for transfer_id in transfer_ids:
        num_items = random.randint(1, 20)

        selected_products = random.sample(product_ids, num_items)

        for product_id in selected_products:
            quantity = random.randint(10, 500)

            transfer_items_data_list.append({
                'transfer_id': transfer_id,
                'product_id': product_id,
                'quantity': quantity
            })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO transfer_items (transfer_id, product_id, quantity)
                VALUES (:transfer_id, :product_id, :quantity)
            """),
            transfer_items_data_list
        )
        conn.commit()

    print(f"добавлено {len(transfer_items_data_list)} записей в таблицу transfer_items")