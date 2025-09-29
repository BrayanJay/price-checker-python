import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price_calculator import find_best_applicable_price, find_all_applicable_prices_for_order


class SampleData:

    #Initiating sample data

    sample_product1_tier_price_list = [
        { "product_id": 1, "tier": "GOLD", "discount_rate": 0.15, "min_qty": 4 },
        { "product_id": 1, "tier": "SILVER", "discount_rate": 0.05, "min_qty": 5 },
        { "product_id": 1, "tier": "PLATINUM", "discount_rate": 0.40, "min_qty": 2 }
    ]

    sample_product1_group_price_list = [
        { "product_id": 1, "group": "REGULAR", "discount_rate": 0.20, "min_qty": 5 },
        { "product_id": 1, "group": "BULK", "discount_rate": 0.10, "min_qty": 10 },
        { "product_id": 1, "group": "VIP", "discount_rate": 0.50, "min_qty": 2 }
    ]

    sample_product_list = [
        { "product_id": 1, "name": "Laptop", "base_price": 350000, "tier_prices": sample_product1_tier_price_list, "group_prices": sample_product1_group_price_list },
        { "product_id": 2, "name": "Smartphone", "base_price": 200000, "tier_prices": [], "group_prices": [] },
        { "product_id": 3, "name": "Tablet", "base_price": 150000, "tier_prices": [], "group_prices": [] }
    ]

    sample_customer1_loyalty_price_list = [
        { "customer_id": 1, "product_id": 2, "discount_rate": 0.20, "min_qty": 5 },
        { "customer_id": 1, "product_id": 1, "discount_rate": 0.10, "min_qty": 10 },
        { "customer_id": 1, "product_id": 3, "discount_rate": 0.50, "min_qty": 2 }
    ]

    sample_customer_list = [
        { "customer_id": 1, "name": "Alice", "tier": "GOLD", "groups": ["BULK", "VIP"], "loyalty_products": sample_customer1_loyalty_price_list },
        { "customer_id": 2, "name": "Bob", "tier": "SILVER", "groups": ["BULK"], "loyalty_products": [] },
        { "customer_id": 3, "name": "Charlie", "tier": "PLATINUM", "groups": ["VIP"], "loyalty_products": [] }
    ]

    sample_order_list = [
        { "product_id": 1, "quantity": 4, "customer_id": 2 },  # Original - should get BASE (no discounts qualify)
        { "product_id": 2, "quantity": 3, "customer_id": 1 },  # Original - should get BASE (loyalty needs qty 5)
        { "product_id": 1, "quantity": 5, "customer_id": 2 },  # Should get TIER discount (SILVER, qty 5)
        { "product_id": 1, "quantity": 3, "customer_id": 3 },  # Should get TIER discount (PLATINUM, qty 2+) and GROUP (VIP, qty 2+)
        { "product_id": 2, "quantity": 5, "customer_id": 1 },  # Should get CUSTOMER/LOYALTY discount
        { "product_id": 1, "quantity": 10, "customer_id": 1 }, # Should get CUSTOMER discount (qty 10) vs TIER (GOLD, qty 4+) vs GROUP (BULK qty 10)
    ]

    sample_test_results_list = []

# Test the functions with the new data structure
if __name__ == "__main__":
    print("=== Testing Price Calculator with New Data Structure ===\n")
    
    # Test with sample orders
    test_orders = SampleData.sample_order_list
    
    print("Sample Orders:")
    for i, order in enumerate(test_orders, 1):
        print(f"{i}. Product {order['product_id']}, Quantity: {order['quantity']}, Customer: {order['customer_id']}")
    
    print("\n\nCalculating Best Prices")
    results = find_best_applicable_price(test_orders, SampleData.sample_product_list, SampleData.sample_customer_list)
    
    for i, result in enumerate(results, 1):
        print(f"Order {i}: {result}")
    
    print("\n\nDetailed Order Results")
    for i, order in enumerate(test_orders, 1):
        print(f"\nOrder {i} - {order}:")
        try:
            detailed_prices = find_all_applicable_prices_for_order(order, SampleData.sample_product_list, SampleData.sample_customer_list)
            print(f"  Base Price: {detailed_prices['base_price']}")
            print(f"  Loyalty Price: {detailed_prices['loyalty_price']}")
            print(f"  Tier Price: {detailed_prices['tier_price']}")
            print(f"  Group Prices: {detailed_prices['group_prices']}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Store results
    SampleData.sample_test_results_list = results
    print(f"\nResults stored in sample_test_results_list: {len(SampleData.sample_test_results_list)} items")