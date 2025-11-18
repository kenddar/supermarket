from sqlalchemy import text
import random
from . import products_data


def seed_products(engine):
    products_data_list = []
    used_names = set()
    used_barcodes = set()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name FROM categories WHERE parent_id IS NOT NULL")
        )
        subcategories = {row.name: row.id for row in result.fetchall()}

    if not subcategories:
        print("таблица categories пуста")
        return

    for subcategory_name, category_id in subcategories.items():

        params = products_data.CATEGORY_PARAMS.get(subcategory_name, {'price': (50, 500), 'expiry': (30, 180)})

        if subcategory_name not in products_data.PRODUCT_NAMES:
            continue

        product_list = products_data.PRODUCT_NAMES[subcategory_name]

        for base in product_list:
            names_to_add = []
            if 'Молоко' in base:
                for percent in products_data.MILK_FAT_PERCENTAGES:
                    names_to_add.append(f"{base} {percent}")
            elif 'Кефир' in base:
                for percent in products_data.MILK_FAT_PERCENTAGES:
                    names_to_add.append(f"{base} {percent}")
            elif 'Сметана' in base:
                for percent in products_data.SOUR_CREAM_FAT_PERCENTAGES:
                    names_to_add.append(f"{base} {percent}")
            elif 'Творог' in base:
                for percent in products_data.COTTAGE_CHEESE_FAT_PERCENTAGES:
                    names_to_add.append(f"{base} {percent}")
            elif 'Масло сливочное' in base:
                for percent in products_data.BUTTER_FAT_PERCENTAGES:
                    names_to_add.append(f"{base} {percent}")
            else:
                names_to_add.append(base)

            for name in names_to_add:
                if name in used_names:
                    continue

                used_names.add(name)

                while True:
                    country_code = random.randint(460, 469)
                    product_code = random.randint(100000000, 999999999)
                    check_digit = random.randint(0, 9)
                    barcode = f"{country_code}{product_code}{check_digit}"

                    if barcode not in used_barcodes:
                        used_barcodes.add(barcode)
                        break

                price = round(random.uniform(*params['price']), 2)
                expiry_days = random.randint(*params['expiry'])

                products_data_list.append({
                    'name': name,
                    'category_id': category_id,
                    'barcode': barcode,
                    'price': price,
                    'expiry_days': expiry_days
                })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO products (name, category_id, barcode, price, expiry_days)
                VALUES (:name, :category_id, :barcode, :price, :expiry_days)
            """),
            products_data_list
        )
        conn.commit()

    print(f"добавлено {len(products_data_list)} записей в таблицу products")