from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/supermarket"

def get_engine():
    return create_engine(DATABASE_URL, echo=False)
