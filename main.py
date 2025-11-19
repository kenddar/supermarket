from config import get_engine
from seeders import (seed_suppliers, seed_customers, seed_categories, seed_products,
                     seed_discounts, seed_shops, seed_stocks)


def main():
    engine = get_engine()

    #seed_suppliers(engine, count=200)
    #seed_customers(engine, count=10000)
    #seed_categories(engine)
    #seed_products(engine)
    #seed_discounts(engine, count=10000)
    #seed_shops(engine, count=250)
    seed_stocks(engine, count=20)


if __name__ == "__main__":
    main()
