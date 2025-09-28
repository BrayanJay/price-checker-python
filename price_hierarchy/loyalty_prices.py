from .price_interface import Price
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.product import Product
from models.customer import Customer
from constants.price import PriceType
from models.place_order import PlaceOrder

class LoyaltyPrices(Price):

    loyalty_prices = []

    def __init__(self, product: Product, customer: Customer, discount_rate: float, min_qty: int, price_type=PriceType.CUSTOMER):
        super().__init__(price_type=price_type, product=product, discount_rate=discount_rate, min_qty=min_qty)
        self.customer = customer

    @staticmethod
    def add_loyalty_price(loyalty_price: 'LoyaltyPrices'):
        LoyaltyPrices.loyalty_prices.append({
            "customer": loyalty_price.customer,
            "product": loyalty_price.product,
            "type": loyalty_price.price_type,
            "discount_rate": loyalty_price.discount_rate,
            "min_qty": loyalty_price.min_qty
        })

    @staticmethod
    def delete_loyalty_price(customer: Customer, product: Product):
        LoyaltyPrices.loyalty_prices = [lp for lp in LoyaltyPrices.loyalty_prices if not (lp['product'] == product and lp['customer'] == customer)]

    @staticmethod
    def get_loyalty_prices():
        for lp in LoyaltyPrices.loyalty_prices:
            print(f"Customer ID: {lp['customer'].customer_id} | Product ID: {lp['product'].product_id} | Price Type: {lp['type']} | Discount Rate: {lp['discount_rate']} | Min Quantity: {lp['min_qty']}")
    
    def calculate_applicable_price(order: PlaceOrder):

        for lp in LoyaltyPrices.loyalty_prices:

            if lp["customer"].customer_id == order.customer_id and lp["product"].product_id == order.product_id:

                if lp["min_qty"] <= order.quantity:
                    applicable_price = order.quantity * lp["product"].base_price * (1 - lp["discount_rate"])
                    return applicable_price

        return None
