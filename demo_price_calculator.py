from data.sample_data import SampleData
from price_calculator import find_best_applicable_price, find_all_applicable_prices_for_order

def demo_price_calculator():
    print("=== Price Calculator Demo ===\n")
    
    # Example orders to test
    test_orders = [
        { "product_id": 1, "quantity": 4, "customer_id": 2 },  # Original request format
        { "product_id": 2, "quantity": 3, "customer_id": 1 },  # Using existing customer
        { "product_id": 1, "quantity": 10, "customer_id": 2 }, # High quantity for BULK discount
        { "product_id": 3, "quantity": 2, "customer_id": 1 },  # Should get loyalty discount
    ]
    
    print("Test Orders:")
    for i, order in enumerate(test_orders, 1):
        print(f"{i}. Product {order['product_id']}, Quantity: {order['quantity']}, Customer: {order['customer_id']}")
    
    print("\n=== Using find_best_applicable_price function ===")
    results = find_best_applicable_price(test_orders, SampleData.products, SampleData.customers)
    
    for i, result in enumerate(results, 1):
        print(f"Order {i}: {result}")
    
    print("\n=== Using find_all_applicable_prices_for_order function ===")
    print("Detailed breakdown for first order:")
    
    first_order = test_orders[0]
    detailed_prices = find_all_applicable_prices_for_order(first_order, SampleData.products, SampleData.customers)
    
    print(f"Order: {first_order}")
    print(f"Base Price: {detailed_prices['base_price']}")
    print(f"Loyalty Price: {detailed_prices['loyalty_price']}")
    print(f"Tier Price: {detailed_prices['tier_price']}")
    print(f"Group Prices: {detailed_prices['group_prices']}")

if __name__ == "__main__":
    demo_price_calculator()