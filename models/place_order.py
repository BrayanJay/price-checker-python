from price_hierarchy.group_prices import GroupedPrices
from price_hierarchy.tiered_prices import TieredPrices
from price_hierarchy.loyalty_prices import LoyaltyPrices


class PlaceOrder:
    placed_orders = []

    def __init__(self, product_id, quantity, customer_id):
        self.product_id = product_id
        self.quantity = quantity
        self.customer_id = customer_id

    def add_order():
        print("Place new order")
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity: "))
        customer_id = int(input("Enter customer ID: "))

        PlaceOrder.placed_orders.append({
            "product_id": product_id,
            "customer_id": customer_id,
            "quantity": quantity
        })
        print("Order Placed Successfully!")

    @staticmethod
    def append_order(order: 'PlaceOrder'):
        PlaceOrder.placed_orders.append({
            "product_id": order.product_id,
            "quantity": order.quantity,
            "customer_id": order.customer_id
        })
        print("Order Placed Successfully!")

    @staticmethod
    def view_orders():
        if not PlaceOrder.placed_orders:
            print("No orders placed.")
        else:
            for order in PlaceOrder.placed_orders:
                print(f"Order - Product ID: {order['product_id']}, Quantity: {order['quantity']}, Customer ID: {order['customer_id']}")