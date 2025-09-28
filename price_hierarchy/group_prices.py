from price_interface import Price
from constants.group import Group

class GroupedPrices(Price):

    grouped_prices = []

    def __init__(self, product_id, amount, group: Group):
        super().__init__(product_id, amount)
        self.group = group

    def __str__(self):
        return f"Product ID: {self.product_id}, Amount: {self.amount}, Group: {self.group.value}"

    @staticmethod
    def add_grouped_price(grouped_price: 'GroupedPrices'):
        GroupedPrices.grouped_prices.append({
            "product_id": grouped_price.product_id,
            "group": grouped_price.group.value,
            "discount_rate": grouped_price.base_price
        })

    @staticmethod
    def delete_grouped_price(product_id, group: Group):
        GroupedPrices.grouped_prices = [gp for gp in GroupedPrices.grouped_prices if not (gp['product_id'] == product_id and gp['group'] == group.value)]

    @staticmethod
    def get_grouped_prices():
        return GroupedPrices.grouped_prices