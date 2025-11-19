from sqlalchemy import text
from faker import Faker
from datetime import date, timedelta
import random
from utils import transliterate_name


def seed_employees(engine, count=200):
    fake = Faker('ru_RU')
    Faker.seed(random.randint(0, 10000))

    employees_data = []
    used_phones = set()
    used_emails = set()

    positions = {
        'Кассир': (25000, 40000),
        'Мерчендайзер': (27000, 45000),
        'Продавец-консультант': (28000, 49000),
        'Товаровед': (35000, 55000),
        'Старший продавец': (40000, 60000),
        'Администратор зала': (45000, 70000),
        'Заведующий отделом': (50000, 80000),
        'Заместитель директора': (70000, 120000),
        'Директор магазина': (90000, 150000),
        'Грузчик': (25000, 35000),
        'Уборщица': (20000, 30000),
        'SMM-специалист': (40000, 65000)
    }

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
            last_name = ''

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

        birth_date = fake.date_of_birth(minimum_age=14, maximum_age=65)

        days_ago = random.randint(0, 365 * 10)
        hire_date = date.today() - timedelta(days=days_ago)

        min_hire_date = birth_date + timedelta(days=365 * 14 + 7)
        if hire_date < min_hire_date:
            hire_date = min_hire_date

        position = random.choice(list(positions.keys()))
        salary_range = positions[position]
        salary = round(random.uniform(salary_range[0], salary_range[1]), 2)

        employees_data.append({
            'full_name': full_name,
            'gender': gender,
            'position': position,
            'salary': salary,
            'email': email,
            'phone_number': phone,
            'birth_date': birth_date,
            'hire_date': hire_date
        })

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO employees (full_name, gender, position, salary, email, phone_number, birth_date, hire_date)
                VALUES (:full_name, :gender, :position, :salary, :email, :phone_number, :birth_date, :hire_date)
            """),
            employees_data
        )
        conn.commit()

    print(f"добавлено {len(employees_data)} записей в таблицу employees")
