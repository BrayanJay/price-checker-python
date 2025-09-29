"""
Test script for the FastAPI Pricing Engine
Run this after starting the API server to test all endpoints
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():

    print("=" * 70)
    print("PRICING ENGINE API TEST SUITE - RESTful Edition")
    print("Testing all 18 endpoints")
    print("=" * 70)
    
    # Test 1: Health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Load sample data
    print("\n3. Loading Sample Data...")
    try:
        response = requests.post(f"{BASE_URL}/load-sample-data")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Get system status
    print("\n4. Getting System Status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Get customers
    print("\n5. Getting Customers...")
    try:
        response = requests.get(f"{BASE_URL}/customers")
        print(f"Status: {response.status_code}")
        customers = response.json()
        print(f"Found {len(customers)} customers:")
        for customer in customers:
            print(f"  - {customer['name']} (ID: {customer['customer_id']}, Tier: {customer['tier']})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Get products
    print("\n6. Getting Products...")
    try:
        response = requests.get(f"{BASE_URL}/products")
        print(f"Status: {response.status_code}")
        products = response.json()
        print(f"Found {len(products)} products:")
        for product in products:
            print(f"  - {product['name']} (ID: {product['product_id']}, Price: LKR {product['base_price']:,})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 7: Calculate single price
    print("\n7. Testing Single Price Calculation...")
    try:
        order_data = {
            "customer_id": 1,
            "product_id": 1,
            "quantity": 5
        }
        response = requests.post(f"{BASE_URL}/calculate-price", json=order_data)
        print(f"Status: {response.status_code}")
        print(f"Order: Customer 1, Product 1, Quantity 5")
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 8: Calculate bulk prices
    print("\n8. Testing Bulk Price Calculation...")
    try:
        bulk_order_data = {
            "orders": [
                {"customer_id": 1, "product_id": 1, "quantity": 2},
                {"customer_id": 2, "product_id": 1, "quantity": 10},
                {"customer_id": 3, "product_id": 1, "quantity": 1},
                {"customer_id": 1, "product_id": 2, "quantity": 5}
            ]
        }
        response = requests.post(f"{BASE_URL}/calculate-bulk-prices", json=bulk_order_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Bulk calculation results:")
        print(f"Total orders processed: {result['total_orders']}")
        for i, order_result in enumerate(result['results'], 1):
            print(f"  Order {i}: {order_result['product_id']} - LKR {order_result['price']:,} ({order_result['price_type']})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 9: Test individual customer lookup
    print("\n9. Testing Individual Customer Lookup...")
    try:
        response = requests.get(f"{BASE_URL}/customers/1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            customer = response.json()
            print(f"Customer Details: {customer['name']} - {customer['tier']} tier, {len(customer['groups'])} groups")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 10: Test individual product lookup
    print("\n10. Testing Individual Product Lookup...")
    try:
        response = requests.get(f"{BASE_URL}/products/1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            product = response.json()
            print(f"Product Details: {product['name']} - LKR {product['base_price']:,}, {product['tier_prices_count']} tier rules, {product['group_prices_count']} group rules")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 11: Create new customer
    print("\n11. Testing Customer Creation...")
    try:
        customer_data = {
            "customer_id": 99,
            "name": "Test Customer",
            "tier": "GOLD",
            "groups": ["VIP"]
        }
        response = requests.post(f"{BASE_URL}/customers", json=customer_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Created customer: {response.json()}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 12: Create new product
    print("\n12. Testing Product Creation...")
    try:
        product_data = {
            "product_id": 99,
            "name": "Test Product",
            "base_price": 50000
        }
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Created product: {response.json()}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 13: Add tier pricing rule
    print("\n13. Testing Tier Pricing Rule Addition...")
    try:
        tier_rule = {
            "product_id": 99,
            "tier": "GOLD",
            "discount_rate": 0.10,
            "min_qty": 2
        }
        response = requests.post(f"{BASE_URL}/products/99/tier-prices", json=tier_rule)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 14: Add group pricing rule
    print("\n14. Testing Group Pricing Rule Addition...")
    try:
        group_rule = {
            "product_id": 99,
            "group": "VIP",
            "discount_rate": 0.15,
            "min_qty": 1
        }
        response = requests.post(f"{BASE_URL}/products/99/group-prices", json=group_rule)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 15: Add loyalty pricing rule
    print("\n15. Testing Loyalty Pricing Rule Addition...")
    try:
        loyalty_rule = {
            "customer_id": 99,
            "product_id": 99,
            "discount_rate": 0.20,
            "min_qty": 1
        }
        response = requests.post(f"{BASE_URL}/customers/99/loyalty-prices", json=loyalty_rule)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 16: Test price calculation with new customer/product
    print("\n16. Testing Price Calculation with New Data...")
    try:
        order_data = {
            "customer_id": 99,
            "product_id": 99,
            "quantity": 2
        }
        response = requests.post(f"{BASE_URL}/calculate-price", json=order_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Best Price: LKR {result['price']:,} ({result['price_type']})")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 17: Get orders
    print("\n17. Testing Order History...")
    try:
        response = requests.get(f"{BASE_URL}/orders")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            orders = response.json()
            print(f"Total orders: {orders['total_orders']}")
            if orders['total_orders'] > 0:
                print("Recent orders:")
                for order in orders['orders'][-3:]:  # Show last 3 orders
                    print(f"  - Order {order['order_id']}: Customer {order['customer_id']}, Product {order['product_id']}, Qty {order['quantity']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 18: Get results
    print("\n18. Testing Calculation Results...")
    try:
        response = requests.get(f"{BASE_URL}/results")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"Total results: {results['total_results']}")
            if results['total_results'] > 0:
                print("Recent results:")
                for result in results['results'][-3:]:  # Show last 3 results
                    print(f"  - {result['product_id']}: LKR {result['price']:,} ({result['price_type']})")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 19: Delete test customer
    print("\n19. Testing Customer Deletion...")
    try:
        response = requests.delete(f"{BASE_URL}/customers/99")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 20: Delete test product
    print("\n20. Testing Product Deletion...")
    try:
        response = requests.delete(f"{BASE_URL}/products/99")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Final status check
    print("\n21. Final System Status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("COMPREHENSIVE API TEST SUITE COMPLETED")
    print("Tested all CRUD operations, pricing rules, and calculations")
    print("=" * 70)

def test_error_scenarios():
    """Test error scenarios and validation"""
    print("\n" + "=" * 70)
    print("TESTING ERROR SCENARIOS & VALIDATION")
    print("=" * 70)
    
    # Test 1: Invalid customer lookup
    print("\n1. Testing Invalid Customer ID Lookup...")
    try:
        response = requests.get(f"{BASE_URL}/customers/999")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Invalid product lookup
    print("\n2. Testing Invalid Product ID Lookup...")
    try:
        response = requests.get(f"{BASE_URL}/products/999")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Duplicate customer creation
    print("\n3. Testing Duplicate Customer Creation...")
    try:
        customer_data = {
            "customer_id": 1,  # This ID already exists
            "name": "Duplicate Customer",
            "tier": "GOLD",
            "groups": ["VIP"]
        }
        response = requests.post(f"{BASE_URL}/customers", json=customer_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Invalid tier in customer creation
    print("\n4. Testing Invalid Tier in Customer Creation...")
    try:
        customer_data = {
            "customer_id": 998,
            "name": "Invalid Tier Customer",
            "tier": "INVALID_TIER",
            "groups": ["VIP"]
        }
        response = requests.post(f"{BASE_URL}/customers", json=customer_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Invalid group in customer creation
    print("\n5. Testing Invalid Group in Customer Creation...")
    try:
        customer_data = {
            "customer_id": 997,
            "name": "Invalid Group Customer",
            "tier": "GOLD",
            "groups": ["INVALID_GROUP"]
        }
        response = requests.post(f"{BASE_URL}/customers", json=customer_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Price calculation with invalid customer
    print("\n6. Testing Price Calculation with Invalid Customer...")
    try:
        order_data = {
            "customer_id": 999,
            "product_id": 1,
            "quantity": 1
        }
        response = requests.post(f"{BASE_URL}/calculate-price", json=order_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 7: Price calculation with invalid product
    print("\n7. Testing Price Calculation with Invalid Product...")
    try:
        order_data = {
            "customer_id": 1,
            "product_id": 999,
            "quantity": 1
        }
        response = requests.post(f"{BASE_URL}/calculate-price", json=order_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 8: Adding pricing rule to non-existent product
    print("\n8. Testing Pricing Rule on Non-existent Product...")
    try:
        tier_rule = {
            "product_id": 999,
            "tier": "GOLD",
            "discount_rate": 0.10,
            "min_qty": 2
        }
        response = requests.post(f"{BASE_URL}/products/999/tier-prices", json=tier_rule)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 9: Invalid JSON payload
    print("\n9. Testing Invalid JSON Payload...")
    try:
        response = requests.post(f"{BASE_URL}/calculate-price", 
                                json={"invalid": "data"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 10: Deleting non-existent customer
    print("\n10. Testing Deletion of Non-existent Customer...")
    try:
        response = requests.delete(f"{BASE_URL}/customers/999")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("ERROR SCENARIO TESTING COMPLETED")
    print("=" * 70)

def test_performance():
    """Test API performance with multiple requests"""
    print("\n" + "=" * 70)
    print("PERFORMANCE TESTING")
    print("=" * 70)
    
    import time
    
    # Test bulk price calculation performance
    print("\n1. Testing Bulk Price Calculation Performance...")
    try:
        # Create 10 orders
        bulk_orders = []
        for i in range(10):
            bulk_orders.append({
                "customer_id": (i % 3) + 1,  # Cycle through customers 1, 2, 3
                "product_id": (i % 3) + 1,   # Cycle through products 1, 2, 3
                "quantity": (i % 5) + 1      # Vary quantity 1-5
            })
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/calculate-bulk-prices", 
                               json={"orders": bulk_orders})
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Processed {result['total_orders']} orders in {end_time - start_time:.3f} seconds")
            print(f"Average time per order: {(end_time - start_time) / result['total_orders']:.3f} seconds")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test multiple sequential requests
    print("\n2. Testing Sequential API Calls...")
    try:
        start_time = time.time()
        for i in range(5):
            response = requests.get(f"{BASE_URL}/status")
        end_time = time.time()
        
        print(f"Made 5 status requests in {end_time - start_time:.3f} seconds")
        print(f"Average response time: {(end_time - start_time) / 5:.3f} seconds")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("PERFORMANCE TESTING COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    print("🚀 FASTAPI PRICING ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("This will test all 18+ endpoints including:")
    print("✓ System endpoints (health, status, data management)")
    print("✓ Customer CRUD operations")
    print("✓ Product CRUD operations") 
    print("✓ Pricing rules management")
    print("✓ Price calculations")
    print("✓ Order and result tracking")
    print("✓ Error handling and validation")
    print("✓ Performance testing")
    print("=" * 70)
    print("\nMake sure the API server is running with:")
    print("  uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
    print("  OR: python api/main.py")
    print("\nStarting comprehensive tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    test_api_endpoints()
    test_error_scenarios() 
    test_performance()