from sqlalchemy import text
import random
from datetime import datetime, timedelta


def seed_transfers(engine, count=200):
    transfers_data_list = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM shops")
        )
        shop_ids = [row.id for row in result.fetchall()]

    if not shop_ids:
        print("таблица shops пуста")
        return

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM stocks")
        )
        stock_ids = [row.id for row in result.fetchall()]

    if not stock_ids:
        print("таблица stocks пуста")
        return

    for _ in range(count):
        shop_id = random.choice(shop_ids)
        stock_id = random.choice(stock_ids)

        days_ago = random.randint(0, 365 * 10)
        delivery_time = datetime.now() - timedelta(days=days_ago)

        hours = random.randint(8, 20)
        minutes = random.randint(0, 59)
        delivery_time = delivery_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)

        transfers_data_list.append({
            'shop_id': shop_id,
            'stock_id': stock_id,
            'delivery_time': delivery_time
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO transfers (shop_id, stock_id, delivery_time)
                VALUES (:shop_id, :stock_id, :delivery_time)
            """),
            transfers_data_list
        )
        conn.commit()

    print(f"добавлено {len(transfers_data_list)} записей в таблицу transfers")
