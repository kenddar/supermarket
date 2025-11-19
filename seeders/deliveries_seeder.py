from sqlalchemy import text
import random
from datetime import datetime, timedelta


def seed_deliveries(engine, count=200):
    deliveries_data_list = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM suppliers")
        )
        supplier_ids = [row.id for row in result.fetchall()]

    if not supplier_ids:
        print("таблица suppliers пуста")
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
        supplier_id = random.choice(supplier_ids)
        stock_id = random.choice(stock_ids)

        days_ago = random.randint(0, 365 * 10)
        delivery_time = datetime.now() - timedelta(days=days_ago)

        hours = random.randint(8, 20)
        minutes = random.randint(0, 59)
        delivery_time = delivery_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)

        deliveries_data_list.append({
            'supplier_id': supplier_id,
            'stock_id': stock_id,
            'delivery_time': delivery_time
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO deliveries (supplier_id, stock_id, delivery_time)
                VALUES (:supplier_id, :stock_id, :delivery_time)
            """),
            deliveries_data_list
        )
        conn.commit()

    print(f"добавлено {len(deliveries_data_list)} записей в таблицу deliveries")
