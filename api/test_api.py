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
    """Test all API endpoints"""
    print("=" * 60)
    print("PRICING ENGINE API TEST SUITE")
    print("=" * 60)
    
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
    
    # Test 9: Final status check
    print("\n9. Final System Status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("API TEST SUITE COMPLETED")
    print("=" * 60)

def test_error_scenarios():
    """Test error scenarios"""
    print("\n" + "=" * 60)
    print("TESTING ERROR SCENARIOS")
    print("=" * 60)
    
    # Test with invalid customer
    print("\n1. Testing Invalid Customer ID...")
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
    
    # Test with invalid product
    print("\n2. Testing Invalid Product ID...")
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

if __name__ == "__main__":
    print("Make sure the API server is running with: uvicorn api.main:app --reload")
    print("Or: python api/main.py")
    print("\nStarting tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    test_api_endpoints()
    test_error_scenarios()