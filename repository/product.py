import json
import os
from typing import List
from datetime import datetime

from models.product import Product
from repository.repository import ProductRepository


class ProductJsonRepositoryImpl(ProductRepository):

    def save(self, products: List[Product]):
        serialized_products = list(product.to_dict() for product in products)
        today = datetime.now()
        filename = f"data/products-{today.date().isoformat()}-{today.time().isoformat()}.json"
        print("Saving product info into json file...")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(serialized_products, f, indent=4)
        print("saved success!")


def get_product_repository() -> ProductRepository:
    return ProductJsonRepositoryImpl()
