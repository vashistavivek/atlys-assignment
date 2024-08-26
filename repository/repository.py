from abc import ABC, abstractmethod
from typing import List

from models.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def save(self, products: List[Product]):
        pass
