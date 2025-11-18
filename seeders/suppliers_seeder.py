from sqlalchemy import text
from faker import Faker
import random
import re
from utils import transliterate_name


def company_name_for_email(company_name):
    company_parts = company_name.split()
    if len(company_parts) > 1:
        clean_company = ' '.join(company_parts[1:])
    else:
        clean_company = company_name

    match = re.search(r'(.*?)\s*\((.*?)\)', clean_company)

    if match:
        before_parentheses = match.group(1).strip()
        inside_parentheses = match.group(2).strip()

        before_latin = transliterate_name(before_parentheses.lower())
        inside_latin = transliterate_name(inside_parentheses.lower())
        company_latin = f"{before_latin}_{inside_latin}"
    else:
        company_latin = transliterate_name(clean_company.lower())

    return company_latin


def seed_suppliers(engine, count=200):
    fake = Faker('ru_RU')
    Faker.seed(random.randint(0, 10000))

    suppliers_data = []
    used_phones = set()
    used_emails = set()
    used_inns = set()

    for i in range(count):
        company_name = fake.company()

        company_latin = company_name_for_email(company_name)

        while True:
            domain = fake.free_email_domain()
            suffix = random.randint(1, 999) if random.random() > 0.5 else ''
            email = f"{company_latin}{suffix}@{domain}".lower()

            if email not in used_emails:
                used_emails.add(email)
                break

        while True:
            phone = f"+7{random.randint(9000000000, 9999999999)}"
            if phone not in used_phones:
                used_phones.add(phone)
                break

        while True:
            inn = fake.businesses_inn()
            if inn not in used_inns:
                used_inns.add(inn)
                break

        suppliers_data.append({
            'company_name': company_name,
            'phone_number': phone,
            'email': email,
            'inn': inn
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO suppliers (company_name, phone_number, email, inn)
                VALUES (:company_name, :phone_number, :email, :inn)
            """),
            suppliers_data
        )
        conn.commit()

    print(f"добавлено {len(suppliers_data)} записей в таблицу suppliers")
