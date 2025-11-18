import random
import psycopg

dsn = "dbname=supermarket user=postgres password=postgres host=localhost port=5432"

rows = []
for i in range(1, 101):
    customer_id = i
    card_number = str(i).zfill(13)          # '0000000000001' ... '0000000000100'
    bonuses = random.randint(0, 1000)       # 0..1000
    total_purchase = round(random.uniform(0, 10000), 2)  # 0.00..10000.00
    rows.append((customer_id, card_number, bonuses, total_purchase))

def loyalty_card_inserting(dsn):
with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO loyalty_card (customer_id, card_number, bonuses, total_purchase)
            VALUES (%s, %s, %s, %s)
            """,
            rows,
        )

