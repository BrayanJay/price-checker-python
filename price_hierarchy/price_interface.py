from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.product import Product

class Price(ABC):
    def __init__(self, price_type, product: Product, discount_rate, min_qty: int):
        self.price_type = price_type
        self.product = product
        self.discount_rate = discount_rate
        self.min_qty = min_qty

    @abstractmethod
    def calculate_applicable_price(self):
        pass