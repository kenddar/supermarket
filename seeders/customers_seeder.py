from sqlalchemy import text
from faker import Faker
from datetime import date, timedelta
import random
from utils import transliterate_name


def seed_customers(engine, count=200):
    fake = Faker('ru_RU')
    Faker.seed(random.randint(0, 10000))

    customers_data = []
    used_phones = set()
    used_emails = set()

    for i in range(count):
        gender = random.choice(['м', 'ж'])

        if gender == 'м':
            full_name = fake.name_male()
        else:
            full_name = fake.name_female()

        name_parts = full_name.split()
        if len(name_parts) >= 2:
            first_name = transliterate_name(name_parts[1].lower())
            last_name = transliterate_name(name_parts[0].lower())
        else:
            first_name = transliterate_name(name_parts[0].lower())
            last_name = 'user'

        while True:
            domain = fake.free_email_domain()
            suffix = random.randint(1, 999) if random.random() > 0.5 else ''
            email = f"{first_name}_{last_name}{suffix}@{domain}".lower()
            if email not in used_emails:
                used_emails.add(email)
                break

        while True:
            phone = f"+7{random.randint(9000000000, 9999999999)}"
            if phone not in used_phones:
                used_phones.add(phone)
                break

        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=100)

        days_ago = random.randint(0, 365 * 10)
        registration_date = date.today() - timedelta(days=days_ago)

        customers_data.append({
            'full_name': full_name,
            'gender': gender,
            'phone_number': phone,
            'email': email,
            'birth_date': birth_date,
            'registration_date': registration_date
        })


    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO customers (full_name, gender, phone_number, email, birth_date, registration_date)
                VALUES (:full_name, :gender, :phone_number, :email, :birth_date, :registration_date)
            """),
            customers_data
        )
        conn.commit()

    print(f"добавлено {len(customers_data)} записей в таблицу customers")
