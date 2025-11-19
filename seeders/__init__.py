from .suppliers_seeder import seed_suppliers
from .customers_seeder import seed_customers
from .categories_seeder import seed_categories
from .products_seeder import seed_products
from .discounts_seeder import seed_discounts
from .shops_seeder import seed_shops
from .stocks_seeder import seed_stocks
from .deliveries_seeder import seed_deliveries
from .transfers_seeder import seed_transfers

__all__ = [
    'seed_suppliers',
    'seed_customers',
    'seed_categories',
    'seed_products',
    'seed_discounts',
    'seed_shops',
    'seed_stocks',
    'seed_deliveries',
    'seed_transfers'
]
