from sqlalchemy import text
from faker import Faker
import re
from utils import transliterate_name


def city_name_for_email(city_name):
    match = re.search(r'(.*?)\s*\((.*?)\)', city_name)

    if match:
        clean_city = match.group(1).strip()
    else:
        clean_city = city_name.strip()
    clean_city = clean_city.replace(' ', '_').replace('-', '_')
    city_latin = transliterate_name(clean_city.lower())

    return city_latin


def seed_shops(engine, count=200):
    fake = Faker('ru_RU')
    shops_data_list = []
    used_emails = set()

    for i in range(count):
        city = fake.city_name()
        address = fake.street_address()

        while True:
            domain = fake.free_email_domain()
            city_latin = city_name_for_email(city)

            address_clean = re.sub(r'^(ул\.|пр\.|алл\.|бул\.|наб\.|пер\.|ш\.)\s*', '', address)
            first_word = address_clean.split(',')[0].split()[0]
            street_latin = transliterate_name(first_word.lower())

            email = f"shop_{city_latin}_{street_latin}@{domain}".lower()

            if email not in used_emails:
                used_emails.add(email)
                break

        shops_data_list.append({
            'city': city,
            'address': address,
            'email': email
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO shops (city, address, email)
                VALUES (:city, :address, :email)
            """),
            shops_data_list
        )
        conn.commit()

    print(f"добавлено {len(shops_data_list)} записей в таблицу shops")