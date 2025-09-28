from .price_interface import Price
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants.tier import Tier
from models.product import Product
from constants.price import PriceType
from models.place_order import PlaceOrder

class TieredPrices(Price):

    tiered_prices = []

    def __init__(self, product: Product, tier: Tier, discount_rate: float, min_qty: int, price_type=PriceType.TIER):
        super().__init__(price_type=price_type, product=product, discount_rate=discount_rate, min_qty=min_qty)
        self.tier = tier

    def __str__(self):
        return f"Product ID: {self.product.product_id}, Product Name: {self.product.name}, Price Type: {self.price_type.value}, Tier Type: {self.tier.value}, Discount Rate: {self.discount_rate}, Min Quantity: {self.min_qty}"

    @staticmethod
    def add_tiered_price(tiered_price: 'TieredPrices'):
        TieredPrices.tiered_prices.append({
            "product": tiered_price.product,
            "type": tiered_price.price_type,
            "tier": tiered_price.tier,
            "discount_rate": tiered_price.discount_rate,
            "min_qty": tiered_price.min_qty
        })

    @staticmethod
    def delete_tiered_price(product: Product, tier: Tier):
        TieredPrices.tiered_prices = [tp for tp in TieredPrices.tiered_prices if not (tp['product'] == product and tp['tier'] == tier.value)]

    @staticmethod
    def get_tiered_prices():
        for tp in TieredPrices.tiered_prices:
            print(f"Product ID: {tp['product'].product_id} | Price Type: {tp['type']} | Tier Type: {tp['tier']} | Discount Rate: {tp['discount_rate']} | Min Quantity: {tp['min_qty']}")

    def calculate_applicable_price(order: PlaceOrder):

        for tp in TieredPrices.tiered_prices:

            if tp["customer"].customer_id == order.customer_id and tp["product"].product_id == order.product_id:

                if tp["min_qty"] <= order.quantity:
                    applicable_price = order.quantity * tp["product"].base_price * (1 - tp["discount_rate"])
                    return applicable_price

        return None