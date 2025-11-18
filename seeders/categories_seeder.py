from sqlalchemy import text


def seed_categories(engine):
    categories_hierarchy = [
        {'name': 'Овощи и фрукты', 'parent_id': None},
        {'name': 'Молочные продукты и яйца', 'parent_id': None},
        {'name': 'Хлеб и выпечка', 'parent_id': None},
        {'name': 'Мясо и рыба', 'parent_id': None},
        {'name': 'Замороженные продукты', 'parent_id': None},
        {'name': 'Напитки', 'parent_id': None},
        {'name': 'Кондитерские изделия', 'parent_id': None},
        {'name': 'Снеки', 'parent_id': None},
        {'name': 'Бакалея', 'parent_id': None},
        {'name': 'Бытовая химия', 'parent_id': None},
    ]

    subcategories = {
        'Овощи и фрукты': [
            'Свежие фрукты и ягоды',
            'Свежие овощи и грибы',
            'Зелень'
        ],
        'Молочные продукты и яйца': [
            'Молоко',
            'Кисломолочные продукты',
            'Сыры',
            'Масло и маргарин',
            'Яйца'
        ],
        'Хлеб и выпечка': [
            'Хлеб',
            'Батоны и багеты',
            'Сдобная выпечка',
            'Торты и пирожные',
            'Хлебцы и сушки'
        ],
        'Мясо и рыба': [
            'Мясо и птица',
            'Колбасные изделия',
            'Рыба и дары моря'
        ],
        'Замороженные продукты': [
            'Мороженое',
            'Замороженные овощи',
            'Замороженные полуфабрикаты',
            'Замороженная рыба'
        ],
        'Напитки': [
            'Вода',
            'Соки и морсы',
            'Газированные напитки',
            'Алкогольные напитки'
        ],
        'Кондитерские изделия': [
            'Шоколад',
            'Конфеты',
            'Вафли и печенье',
            'Мармелад и зефир',
            'Варенье и мед'
        ],
        'Снеки': [
            'Чипсы и сухарики',
            'Орехи и сухофрукты'
            'Соленые снеки и сухофрукты'
        ],
        'Бакалея': [
            'Крупы и макароны',
            'Мука и сахар',
            'Растительное масло',
            'Чай и кофе',
            'Консервы',
            'Масло, соусы и приправы'
        ],
        'Бытовая химия': [
            'Моющие средства',
            'Средства для стирки',
            'Средства гигиены',
            'Средства для уборки'
        ]
    }

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO categories (name, parent_id)
                VALUES (:name, :parent_id)
            """),
            categories_hierarchy
        )
        conn.commit()

        print(f"добавлено {len(categories_hierarchy)} корневых категорий")

        result = conn.execute(
            text("SELECT id, name FROM categories WHERE parent_id IS NULL")
        )
        parent_categories = {row.name: row.id for row in result.fetchall()}

        subcategories_data = []
        for parent_name, children in subcategories.items():
            parent_id = parent_categories.get(parent_name)
            if parent_id:
                for child_name in children:
                    subcategories_data.append({
                        'name': child_name,
                        'parent_id': parent_id
                    })

        if subcategories_data:
            conn.execute(
                text("""
                    INSERT INTO categories (name, parent_id)
                    VALUES (:name, :parent_id)
                """),
                subcategories_data
            )
            conn.commit()

            print(f"добавлено {len(subcategories_data)} подкатегорий")

    total = len(categories_hierarchy) + len(subcategories_data)
    print(f"✓ всего {total} категорий добавлено в таблицу categories")
