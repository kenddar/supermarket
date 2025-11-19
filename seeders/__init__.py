from .suppliers_seeder import seed_suppliers
from .customers_seeder import seed_customers
from .categories_seeder import seed_categories
from .products_seeder import seed_products
from .discounts_seeder import seed_discounts
from .shops_seeder import seed_shops

__all__ = [
    'seed_suppliers',
    'seed_customers',
    'seed_categories',
    'seed_products',
    'seed_discounts',
    'seed_shops'
]
