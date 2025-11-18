from config import get_engine
from seeders import seed_suppliers, seed_customers


def main():
    engine = get_engine()

    seed_suppliers(engine, count=200)
    seed_customers(engine, count=10000)


if __name__ == "__main__":
    main()
