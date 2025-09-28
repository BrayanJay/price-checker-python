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
            "quantity": quantity,
            "customer_id": customer_id
        })
        print("Order Placed Successfully!")

    @staticmethod
    def view_orders():
        if not PlaceOrder.placed_orders:
            print("No orders placed.")
        else:
            for order in PlaceOrder.placed_orders:
                print(f"Order - Product ID: {order.product_id}, Quantity: {order.quantity}, Customer ID: {order.customer_id}")