from sqlalchemy import text
import random


def seed_employee_workplaces(engine):
    workplaces_data = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM employees")
        )
        employee_ids = [row.id for row in result.fetchall()]

    if not employee_ids:
        print("таблица employees пуста")
        return

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

    day_schedules = ["2/2", "5/2", "3/3"]
    time_schedules = [
        "09:00-21:00",
        "09:00-18:00",
        "12:00-21:00",
        "08:00-20:00",
        "08:00-17:00",
        "10:00-19:00",
        "07:00-16:00",
    ]

    for employee_id in employee_ids:
        if random.random() < 0.7:
            shop_id = random.choice(shop_ids)
            stock_id = None
        else:
            shop_id = None
            stock_id = random.choice(stock_ids)

        days = random.choice(day_schedules)
        hours = random.choice(time_schedules)
        schedule = f"{days} {hours}"

        workplaces_data.append({
            "employee_id": employee_id,
            "shop_id": shop_id,
            "stock_id": stock_id,
            "schedule": schedule,
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO employee_workplaces (employee_id, shop_id, stock_id, schedule)
                VALUES (:employee_id, :shop_id, :stock_id, :schedule)
            """),
            workplaces_data
        )
        conn.commit()

    print(f"добавлено {len(workplaces_data)} записей в таблицу employee_workplaces")