from price_interface import Price
from constants.tier import Tier

class TieredPrices(Price):

    tiered_prices = []

    def __init__(self, product_id, amount, tier: Tier):
        super().__init__(product_id, amount)
        self.tier = tier

    def __str__(self):
        return f"Product ID: {self.product_id}, Amount: {self.amount}, Tier: {self.tier.value}"
    
    @staticmethod
    def add_tiered_price(tiered_price: 'TieredPrices'):
        TieredPrices.tiered_prices.append({
            "product_id": tiered_price.product_id,
            "tier": tiered_price.tier.value,
            "discount_rate": tiered_price.base_price
        })

    @staticmethod
    def delete_tiered_price(product_id, tier: Tier):
        TieredPrices.tiered_prices = [tp for tp in TieredPrices.tiered_prices if not (tp['product_id'] == product_id and tp['tier'] == tier.value)]

    @staticmethod
    def get_tiered_prices():
        return TieredPrices.tiered_prices