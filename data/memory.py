import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.customer import Customer
from models.product import Product
from price_hierarchy.loyalty_prices import LoyaltyPrices
from price_hierarchy.tiered_prices import TieredPrices
from price_hierarchy.group_prices import GroupedPrices


class Memory:

    customers = []  # Type will be - [[Customer, LoyaltyPrice]]
    products = []   # Type will be - [[Product, TierPrices, GroupPrices]]
    orders = []     # Type will be - [{"customer_id": , "product_id": , "quantity": }]
    results = []    # Type will be - [{"product_id": , "price":, "price_type"}]
    
    @classmethod
    def add_customer_with_loyalty(cls, customer: Customer, loyalty_prices: list = None):

        if loyalty_prices is None:
            loyalty_prices = []
        cls.customers.append([customer, loyalty_prices])
    
    @classmethod
    def add_product_with_pricing(cls, product: Product, tier_prices: list = None, group_prices: list = None):

        if tier_prices is None:
            tier_prices = []
        if group_prices is None:
            group_prices = []
        cls.products.append([product, tier_prices, group_prices])
    
    @classmethod
    def add_order(cls, customer_id: int, product_id: int, quantity: int):

        order = {
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity
        }
        cls.orders.append(order)
    
    @classmethod
    def add_result(cls, product_id: str, price: int, price_type: str):

        result = {
            "product_id": product_id,
            "price": price,
            "price_type": price_type
        }
        cls.results.append(result)
    
    @classmethod
    def get_customer_by_id(cls, customer_id: int):

        for customer_data in cls.customers:
            customer, loyalty_prices = customer_data
            if customer.customer_id == customer_id:
                return customer_data
        return None
    
    @classmethod
    def get_product_by_id(cls, product_id: int):

        for product_data in cls.products:
            product, tier_prices, group_prices = product_data
            if product.product_id == product_id:
                return product_data
        return None
    
    @classmethod
    def get_all_customers(cls):

        customers_dict = []
        for customer_data in cls.customers:
            customer, loyalty_prices = customer_data
            customer_dict = {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "tier": customer.tier.value,
                "groups": [group.value for group in customer.groups],
                "loyalty_products": loyalty_prices
            }
            customers_dict.append(customer_dict)
        return customers_dict
    
    @classmethod
    def get_all_products(cls):

        products_dict = []
        for product_data in cls.products:
            product, tier_prices, group_prices = product_data
            product_dict = {
                "product_id": product.product_id,
                "name": product.name,
                "base_price": product.base_price,
                "tier_prices": tier_prices,
                "group_prices": group_prices
            }
            products_dict.append(product_dict)
        return products_dict
    
    @classmethod
    def view_customers(cls):

        if not cls.customers:
            print("No customers found.")
            return
        
        for i, customer_data in enumerate(cls.customers, 1):
            customer, loyalty_prices = customer_data
            print(f"{i}. Customer ID: {customer.customer_id}")
            print(f"   Name: {customer.name}")
            print(f"   Tier: {customer.tier.value}")
            print(f"   Groups: {[group.value for group in customer.groups]}")
            print(f"   Loyalty Prices: {len(loyalty_prices)} rules")
            for lp in loyalty_prices:
                print(f"     Product {lp['product_id']}: {lp['discount_rate']*100}% off, min qty {lp['min_qty']}")
            print()
    
    @classmethod
    def view_products(cls):

        if not cls.products:
            print("No products found.")
            return
        
        for i, product_data in enumerate(cls.products, 1):
            product, tier_prices, group_prices = product_data
            print(f"{i}. Product ID: {product.product_id}")
            print(f"   Name: {product.name}")
            print(f"   Base Price: {product.base_price}")
            print(f"   Tier Prices: {len(tier_prices)} rules")
            for tp in tier_prices:
                print(f"     {tp['tier']}: {tp['discount_rate']*100}% off, min qty {tp['min_qty']}")
            print(f"   Group Prices: {len(group_prices)} rules")
            for gp in group_prices:
                print(f"     {gp['group']}: {gp['discount_rate']*100}% off, min qty {gp['min_qty']}")
            print()
    
    @classmethod
    def view_orders(cls):

        if not cls.orders:
            print("No orders found.")
            return
        
        for i, order in enumerate(cls.orders, 1):
            print(f"{i}. Customer ID: {order['customer_id']}, Product ID: {order['product_id']}, Quantity: {order['quantity']}")
    
    @classmethod
    def view_results(cls):

        if not cls.results:
            print("No results found.")
            return
        
        for i, result in enumerate(cls.results, 1):
            print(f"{i}. Product ID: {result['product_id']}, Price: {result['price']}, Type: {result['price_type']}")
    
    @classmethod
    def clear_all(cls):
        cls.customers.clear()
        cls.products.clear()
        cls.orders.clear()
        cls.results.clear()
        print("All data cleared from memory.")