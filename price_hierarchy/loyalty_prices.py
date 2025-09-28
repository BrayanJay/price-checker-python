class LoyaltyPrices:

    loyalty_prices = []

    def __init__(self, customer_id, product_id, discount_rate):
        self.customer_id = customer_id
        self.product_id = product_id
        self.discount_rate = discount_rate

    @staticmethod
    def add_loyalty_price(customer_id, product_id, discount_rate):
        LoyaltyPrices.loyalty_prices.append({
            "customer_id": customer_id,
            "product_id": product_id,
            "discount_rate": discount_rate
        })

    @staticmethod
    def get_loyalty_prices():
        return LoyaltyPrices.loyalty_prices