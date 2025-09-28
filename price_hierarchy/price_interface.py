from abc import ABC, abstractmethod

class Price(ABC):
    def __init__(self, product_id, base_price):
        self.product_id = product_id
        self.base_price = base_price