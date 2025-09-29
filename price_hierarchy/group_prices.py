from .price_interface import Price
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants.group import Group
from models.product import Product
from constants.price import PriceType

class GroupedPrices(Price):

    grouped_prices = []

    def __init__(self, product: Product, group: Group, discount_rate: float, min_qty: int, price_type=PriceType.GROUP):
        super().__init__(price_type=price_type, product=product, discount_rate=discount_rate, min_qty=min_qty)
        self.group = group

    def __str__(self):
        return f"Product ID: {self.product.product_id}, Product Name: {self.product.name}, Price Type: {self.price_type.value}, Group Type: {self.group.value}, Discount Rate: {self.discount_rate}, Min Quantity: {self.min_qty}"

    @staticmethod
    def add_grouped_price(grouped_price: 'GroupedPrices'):
        GroupedPrices.grouped_prices.append({
            "product": grouped_price.product,
            "type": grouped_price.price_type,
            "group": grouped_price.group,
            "discount_rate": grouped_price.discount_rate,
            "min_qty": grouped_price.min_qty
        })

    @staticmethod
    def delete_grouped_price(product: Product, group: Group):
        GroupedPrices.grouped_prices = [gp for gp in GroupedPrices.grouped_prices if not (gp['product'] == product and gp['group'] == group.value)]

    @staticmethod
    def get_grouped_prices():
        for gp in GroupedPrices.grouped_prices:
            print(f"Product ID: {gp['product'].product_id} | Price Type: {gp['type']} | Group Type: {gp['group']} | Discount Rate: {gp['discount_rate']} | Min Quantity: {gp['min_qty']}")

    def calculate_applicable_price(order):

        for gp in GroupedPrices.grouped_prices:

            if gp["customer"].customer_id == order.customer_id and gp["product"].product_id == order.product_id:

                if gp["min_qty"] <= order.quantity:
                    applicable_price = order.quantity * gp["product"].base_price * (1 - gp["discount_rate"])
                    return applicable_price

        return None