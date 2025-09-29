from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.memory import Memory
from models.customer import Customer
from models.product import Product
from constants.group import Group
from constants.tier import Tier
from price_calculator import find_best_applicable_price

app = FastAPI(
    title="Pricing Engine API",
    description="A FastAPI application for dynamic pricing with tier, group, and loyalty discounts",
    version="2.0.0"
)

# Pydantic models for request/response
class OrderRequest(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    product_id: str
    price: int
    price_type: str

class BulkOrderRequest(BaseModel):
    orders: List[OrderRequest]

class BulkOrderResponse(BaseModel):
    results: List[OrderResponse]
    total_orders: int

class CustomerInfo(BaseModel):
    customer_id: int
    name: str
    tier: str
    groups: List[str]
    loyalty_products_count: int

class ProductInfo(BaseModel):
    product_id: int
    name: str
    base_price: float
    tier_prices_count: int
    group_prices_count: int

class SystemStatus(BaseModel):
    customers_count: int
    products_count: int
    orders_count: int
    results_count: int
    sample_data_loaded: bool

# Initialize the API
@app.on_event("startup")
async def startup_event():
    # Initialize the system on startup
    Memory.clear_all()
    print("Pricing Engine API started - Memory cleared")

@app.get("/")
async def root():
    # Root endpoint with API information
    return {
        "message": "Welcome to Pricing Engine API v2.0",
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "load_sample_data": "POST /load-sample-data",
            "calculate_price": "POST /calculate-price",
            "calculate_bulk_prices": "POST /calculate-bulk-prices",
            "get_customers": "GET /customers",
            "get_products": "GET /products",
            "get_status": "GET /status"
        }
    }

@app.get("/health")
async def health_check():
    # Health check endpoint
    return {
        "status": "healthy",
        "timestamp": "2025-09-29",
        "version": "2.0.0"
    }

@app.post("/load-sample-data")
async def load_sample_data():
    # Load sample data for testing
    try:
        # Clear existing data
        Memory.clear_all()
        
        # Add sample products
        product1 = Product(1, "Gaming Laptop", 350000)
        product2 = Product(2, "Smartphone", 200000)
        product3 = Product(3, "Tablet", 150000)
        
        # Add products with pricing rules
        tier_prices_p1 = [
            {"product_id": 1, "tier": "GOLD", "discount_rate": 0.15, "min_qty": 4},
            {"product_id": 1, "tier": "SILVER", "discount_rate": 0.05, "min_qty": 5},
            {"product_id": 1, "tier": "PLATINUM", "discount_rate": 0.40, "min_qty": 2}
        ]
        
        group_prices_p1 = [
            {"product_id": 1, "group": "REGULAR", "discount_rate": 0.20, "min_qty": 5},
            {"product_id": 1, "group": "BULK", "discount_rate": 0.10, "min_qty": 10},
            {"product_id": 1, "group": "VIP", "discount_rate": 0.50, "min_qty": 2}
        ]
        
        Memory.add_product_with_pricing(product1, tier_prices_p1, group_prices_p1)
        Memory.add_product_with_pricing(product2)
        Memory.add_product_with_pricing(product3)
        
        # Add sample customers
        customer1 = Customer(1, "Alice Premium", Tier.GOLD, [Group.BULK, Group.VIP])
        customer2 = Customer(2, "Bob Business", Tier.SILVER, [Group.BULK])
        customer3 = Customer(3, "Charlie Elite", Tier.PLATINUM, [Group.VIP])
        
        # Add customers with loyalty pricing
        loyalty_prices_c1 = [
            {"customer_id": 1, "product_id": 2, "discount_rate": 0.20, "min_qty": 5},
            {"customer_id": 1, "product_id": 1, "discount_rate": 0.10, "min_qty": 10},
            {"customer_id": 1, "product_id": 3, "discount_rate": 0.50, "min_qty": 2}
        ]
        
        Memory.add_customer_with_loyalty(customer1, loyalty_prices_c1)
        Memory.add_customer_with_loyalty(customer2)
        Memory.add_customer_with_loyalty(customer3)
        
        return {
            "message": "Sample data loaded successfully",
            "data": {
                "customers": len(Memory.customers),
                "products": len(Memory.products),
                "pricing_rules": {
                    "loyalty": len(loyalty_prices_c1),
                    "tier": len(tier_prices_p1),
                    "group": len(group_prices_p1)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sample data: {str(e)}")

@app.post("/calculate-price", response_model=OrderResponse)
async def calculate_price(order: OrderRequest):
    # Calculate the best applicable price for a single order
    try:
        # Validate that customers and products exist
        if not Memory.customers:
            raise HTTPException(status_code=400, detail="No customers found. Please load sample data first.")
        
        if not Memory.products:
            raise HTTPException(status_code=400, detail="No products found. Please load sample data first.")
        
        # Convert to the format expected by price calculator
        order_dict = {
            "customer_id": order.customer_id,
            "product_id": order.product_id,
            "quantity": order.quantity
        }
        
        # Get data in dictionary format for price calculator
        customers_dict = Memory.get_all_customers()
        products_dict = Memory.get_all_products()
        
        # Calculate best price
        results = find_best_applicable_price([order_dict], products_dict, customers_dict)
        
        if not results:
            raise HTTPException(status_code=500, detail="No price calculated")
        
        result = results[0]
        
        # Store the order and result in memory
        Memory.add_order(order.customer_id, order.product_id, order.quantity)
        Memory.add_result(result['product_id'], result['price'], result['price_type'])
        
        return OrderResponse(
            product_id=result['product_id'],
            price=result['price'],
            price_type=result['price_type']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating price: {str(e)}")

@app.post("/calculate-bulk-prices", response_model=BulkOrderResponse)
async def calculate_bulk_prices(bulk_request: BulkOrderRequest):
    # Calculate the best applicable prices for multiple orders
    try:
        if not Memory.customers:
            raise HTTPException(status_code=400, detail="No customers found. Please load sample data first.")
        
        if not Memory.products:
            raise HTTPException(status_code=400, detail="No products found. Please load sample data first.")
        
        # Convert orders to dictionary format
        orders_dict = []
        for order in bulk_request.orders:
            orders_dict.append({
                "customer_id": order.customer_id,
                "product_id": order.product_id,
                "quantity": order.quantity
            })
        
        # Get data in dictionary format for price calculator
        customers_dict = Memory.get_all_customers()
        products_dict = Memory.get_all_products()
        
        # Calculate best prices
        results = find_best_applicable_price(orders_dict, products_dict, customers_dict)
        
        # Store orders and results in memory
        for order_dict, result in zip(orders_dict, results):
            Memory.add_order(order_dict['customer_id'], order_dict['product_id'], order_dict['quantity'])
            Memory.add_result(result['product_id'], result['price'], result['price_type'])
        
        # Convert results to response format
        response_results = []
        for result in results:
            response_results.append(OrderResponse(
                product_id=result['product_id'],
                price=result['price'],
                price_type=result['price_type']
            ))
        
        return BulkOrderResponse(
            results=response_results,
            total_orders=len(results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating bulk prices: {str(e)}")

@app.get("/customers", response_model=List[CustomerInfo])
async def get_customers():
    # Get all customers with their information
    try:
        customers_info = []
        for customer_data in Memory.customers:
            customer, loyalty_prices = customer_data
            customers_info.append(CustomerInfo(
                customer_id=customer.customer_id,
                name=customer.name,
                tier=customer.tier.value,
                groups=[group.value for group in customer.groups],
                loyalty_products_count=len(loyalty_prices)
            ))
        
        return customers_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving customers: {str(e)}")

@app.get("/products", response_model=List[ProductInfo])
async def get_products():
    # Get all products with their information
    try:
        products_info = []
        for product_data in Memory.products:
            product, tier_prices, group_prices = product_data
            products_info.append(ProductInfo(
                product_id=product.product_id,
                name=product.name,
                base_price=product.base_price,
                tier_prices_count=len(tier_prices),
                group_prices_count=len(group_prices)
            ))
        
        return products_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")

@app.get("/status", response_model=SystemStatus)
async def get_status():
    # Get system status and data counts
    try:
        return SystemStatus(
            customers_count=len(Memory.customers),
            products_count=len(Memory.products),
            orders_count=len(Memory.orders),
            results_count=len(Memory.results),
            sample_data_loaded=len(Memory.customers) > 0 and len(Memory.products) > 0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving status: {str(e)}")

@app.delete("/clear-data")
async def clear_data():
    # Clear all data from memory
    try:
        Memory.clear_all()
        return {"message": "All data cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)