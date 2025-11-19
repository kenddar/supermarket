from sqlalchemy import text
import random
from datetime import date, timedelta


def seed_discounts(engine, count=10000):
    discounts_data_list = []

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM products")
        )
        product_ids = [row.id for row in result.fetchall()]

    if not product_ids:
        print("таблица products пуста")
        return

    universal_discounts = [
        'Скидка недели',
        'Специальное предложение',
        'Акция выходного дня',
        'Мега скидка',
        'Супер цена',
        'Распродажа',
        'Снижение цен',
        'Невероятная скидка',
        'Выгодное предложение',
        'Лучшая цена',
        'Скидка для всех'
    ]

    period_discounts = {
        'winter': {
            'names': [
                'Новогодняя распродажа',
                'Рождественские скидки',
                'Зимняя акция',
                'Новогодние предложения',
                'Морозная распродажа',
                'Зимние скидки',
                'Рождественские чудеса',
                'Новый год - новые цены'
            ],
            'months': [12, 1, 2]
        },
        'spring': {
            'names': [
                'Весенняя распродажа',
                'Весенние скидки',
                'Весеннее обновление цен',
                'Весенняя свежесть'
            ],
            'months': [3, 4, 5]
        },
        'summer': {
            'names': [
                'Летняя акция',
                'Летние скидки',
                'Жаркие предложения',
                'Летняя распродажа',
                'Пляжный сезон - скидки',
                'Летнее предложение'
            ],
            'months': [6, 7, 8]
        },
        'autumn': {
            'names': [
                'Осенняя распродажа',
                'Осенние скидки',
                'Школьная распродажа',
                'Осеннее предложение',
                'Золотая осень - золотые цены',
            ],
            'months': [9, 10, 11]
        }
    }

    date_specific_discounts = [
        ('Скидки к 8 Марта', 3, 8),
        ('Женский день - скидки', 3, 8),
        ('23 февраля - скидки', 2, 23),
        ('День победы - акция', 5, 9),
        ('День России - скидки', 6, 12),
        ('Черная пятница', 11, 11),
    ]

    discount_ranges = [
        (5, 10),
        (10, 20),
        (15, 30),
        (25, 40),
        (35, 50),
        (40, 70),
    ]
    discount_weights = [0.40, 0.30, 0.20, 0.07, 0.02, 0.01]

    for _ in range(count):
        product_id = random.choice(product_ids)

        discount_range = random.choices(discount_ranges, weights=discount_weights)[0]
        value = random.randint(*discount_range)

        days_ago = random.randint(0, 365 * 10)
        random_date = date.today() - timedelta(days=days_ago)
        year = random_date.year

        discount_type = random.choice(['universal', 'period', 'date_specific'])

        if discount_type == 'universal':
            if random.random() < 0.2:
                name = None
            else:
                name = random.choice(universal_discounts)

            start_date = random_date

            duration_ranges = [3, 5, 7, 10, 14, 21, 30]
            duration_weights = [0.05, 0.10, 0.30, 0.25, 0.20, 0.07, 0.03]
            duration = random.choices(duration_ranges, weights=duration_weights)[0]
            end_date = start_date + timedelta(days=duration)

        elif discount_type == 'period':
            season = random.choice(list(period_discounts.keys()))
            name = random.choice(period_discounts[season]['names'])

            allowed_months = period_discounts[season]['months']
            month = random.choice(allowed_months)

            if month == 2:
                max_day = 28
            elif month in [4, 6, 9, 11]:
                max_day = 30
            else:
                max_day = 31

            day = random.randint(1, max_day)

            start_date = date(year, month, day)

            duration = random.choice([7, 10, 14, 21])
            end_date = start_date + timedelta(days=duration)

        else:
            discount_name, month, day = random.choice(date_specific_discounts)
            name = discount_name

            target_date = date(year, month, day)

            start_date = target_date - timedelta(days=7)
            end_date = target_date + timedelta(days=7)

        discounts_data_list.append({
            'product_id': product_id,
            'value': value,
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO discounts (product_id, value, name, start_date, end_date)
                VALUES (:product_id, :value, :name, :start_date, :end_date)
            """),
            discounts_data_list
        )
        conn.commit()

    print(f"добавлено {len(discounts_data_list)} записей в таблицу discounts")