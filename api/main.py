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

# FastAPI app is now created above with lifespan

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

# Additional Pydantic models for CRUD operations
class CustomerCreate(BaseModel):
    customer_id: int
    name: str
    tier: str
    groups: List[str]

class ProductCreate(BaseModel):
    product_id: int
    name: str
    base_price: float

class TierPriceRule(BaseModel):
    product_id: int
    tier: str
    discount_rate: float
    min_qty: int

class GroupPriceRule(BaseModel):
    product_id: int
    group: str
    discount_rate: float
    min_qty: int

class LoyaltyPriceRule(BaseModel):
    customer_id: int
    product_id: int
    discount_rate: float
    min_qty: int

class OrderHistory(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    timestamp: str

# Initialize the API using modern lifespan events
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Memory.clear_all()
    print("Pricing Engine API started - Memory cleared")
    yield
    # Shutdown (if needed)
    print("Pricing Engine API shutting down")

app = FastAPI(
    title="Pricing Engine API",
    description="A FastAPI application for dynamic pricing with tier, group, and loyalty discounts",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    # Root endpoint with API information
    return {
        "message": "Welcome to Pricing Engine API v2.0 - RESTful Edition",
        "documentation": "/docs",
        "health": "/health",
        "version": "2.0.0",
        "endpoints": {
            "system": {
                "health": "GET /health",
                "status": "GET /status", 
                "load_sample_data": "POST /load-sample-data",
                "clear_data": "DELETE /clear-data"
            },
            "customers": {
                "list_customers": "GET /customers",
                "get_customer": "GET /customers/{customer_id}",
                "create_customer": "POST /customers",
                "delete_customer": "DELETE /customers/{customer_id}",
                "add_loyalty_pricing": "POST /customers/{customer_id}/loyalty-prices"
            },
            "products": {
                "list_products": "GET /products",
                "get_product": "GET /products/{product_id}",
                "create_product": "POST /products",
                "delete_product": "DELETE /products/{product_id}",
                "add_tier_pricing": "POST /products/{product_id}/tier-prices",
                "add_group_pricing": "POST /products/{product_id}/group-prices"
            },
            "pricing": {
                "calculate_single_price": "POST /calculate-price",
                "calculate_bulk_prices": "POST /calculate-bulk-prices"
            },
            "orders": {
                "get_orders": "GET /orders",
                "get_results": "GET /results"
            }
        },
        "features": [
            "Complete CRUD operations for customers and products",
            "Dynamic pricing rules management",
            "Tier, Group, and Loyalty pricing support",
            "Bulk price calculations",
            "Order tracking and result history",
            "Comprehensive error handling",
            "OpenAPI/Swagger documentation"
        ]
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

# CRUD Operations for Customers
@app.post("/customers", response_model=CustomerInfo)
async def create_customer(customer_data: CustomerCreate):

    try:
        # Validate tier and groups
        tier = Tier(customer_data.tier.upper())
        groups = [Group(g.upper()) for g in customer_data.groups]
        
        # Check if customer already exists
        if Memory.get_customer_by_id(customer_data.customer_id):
            raise HTTPException(status_code=400, detail=f"Customer with ID {customer_data.customer_id} already exists")
        
        # Create customer
        customer = Customer(customer_data.customer_id, customer_data.name, tier, groups)
        Memory.add_customer_with_loyalty(customer)
        
        return CustomerInfo(
            customer_id=customer.customer_id,
            name=customer.name,
            tier=customer.tier.value,
            groups=[group.value for group in customer.groups],
            loyalty_products_count=0
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid tier or group: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")

@app.get("/customers/{customer_id}", response_model=CustomerInfo)
async def get_customer(customer_id: int):

    try:
        customer_data = Memory.get_customer_by_id(customer_id)
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer, loyalty_prices = customer_data
        return CustomerInfo(
            customer_id=customer.customer_id,
            name=customer.name,
            tier=customer.tier.value,
            groups=[group.value for group in customer.groups],
            loyalty_products_count=len(loyalty_prices)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving customer: {str(e)}")

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):

    try:
        customer_data = Memory.get_customer_by_id(customer_id)
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Remove customer from memory
        Memory.customers = [c for c in Memory.customers if c[0].customer_id != customer_id]
        
        return {"message": f"Customer {customer_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting customer: {str(e)}")

# CRUD Operations for Products
@app.post("/products", response_model=ProductInfo)
async def create_product(product_data: ProductCreate):

    try:
        # Check if product already exists
        if Memory.get_product_by_id(product_data.product_id):
            raise HTTPException(status_code=400, detail=f"Product with ID {product_data.product_id} already exists")
        
        # Create product
        product = Product(product_data.product_id, product_data.name, product_data.base_price)
        Memory.add_product_with_pricing(product)
        
        return ProductInfo(
            product_id=product.product_id,
            name=product.name,
            base_price=product.base_price,
            tier_prices_count=0,
            group_prices_count=0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@app.get("/products/{product_id}", response_model=ProductInfo)
async def get_product(product_id: int):

    try:
        product_data = Memory.get_product_by_id(product_id)
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product, tier_prices, group_prices = product_data
        return ProductInfo(
            product_id=product.product_id,
            name=product.name,
            base_price=product.base_price,
            tier_prices_count=len(tier_prices),
            group_prices_count=len(group_prices)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving product: {str(e)}")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):

    try:
        product_data = Memory.get_product_by_id(product_id)
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Remove product from memory
        Memory.products = [p for p in Memory.products if p[0].product_id != product_id]
        
        return {"message": f"Product {product_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

# Pricing Rules Management
@app.post("/products/{product_id}/tier-prices")
async def add_tier_price_rule(product_id: int, rule: TierPriceRule):

    try:
        product_data = Memory.get_product_by_id(product_id)
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product, tier_prices, group_prices = product_data
        
        # Validate tier
        tier = Tier(rule.tier.upper())
        
        # Check if rule already exists
        for tp in tier_prices:
            if tp['tier'] == tier.value:
                raise HTTPException(status_code=400, detail=f"Tier pricing rule for {tier.value} already exists")
        
        # Add new rule
        tier_rule = {
            "product_id": product_id,
            "tier": tier.value,
            "discount_rate": rule.discount_rate,
            "min_qty": rule.min_qty
        }
        tier_prices.append(tier_rule)
        
        return {"message": f"Tier pricing rule added for {tier.value}"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid tier: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding tier pricing rule: {str(e)}")

@app.post("/products/{product_id}/group-prices")
async def add_group_price_rule(product_id: int, rule: GroupPriceRule):

    try:
        product_data = Memory.get_product_by_id(product_id)
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product, tier_prices, group_prices = product_data
        
        # Validate group
        group = Group(rule.group.upper())
        
        # Check if rule already exists
        for gp in group_prices:
            if gp['group'] == group.value:
                raise HTTPException(status_code=400, detail=f"Group pricing rule for {group.value} already exists")
        
        # Add new rule
        group_rule = {
            "product_id": product_id,
            "group": group.value,
            "discount_rate": rule.discount_rate,
            "min_qty": rule.min_qty
        }
        group_prices.append(group_rule)
        
        return {"message": f"Group pricing rule added for {group.value}"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid group: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding group pricing rule: {str(e)}")

@app.post("/customers/{customer_id}/loyalty-prices")
async def add_loyalty_price_rule(customer_id: int, rule: LoyaltyPriceRule):

    try:
        customer_data = Memory.get_customer_by_id(customer_id)
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Validate product exists
        if not Memory.get_product_by_id(rule.product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        
        customer, loyalty_prices = customer_data
        
        # Check if rule already exists
        for lp in loyalty_prices:
            if lp['product_id'] == rule.product_id:
                raise HTTPException(status_code=400, detail=f"Loyalty pricing for product {rule.product_id} already exists")
        
        # Add new rule
        loyalty_rule = {
            "customer_id": customer_id,
            "product_id": rule.product_id,
            "discount_rate": rule.discount_rate,
            "min_qty": rule.min_qty
        }
        loyalty_prices.append(loyalty_rule)
        
        return {"message": f"Loyalty pricing rule added for product {rule.product_id}"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding loyalty pricing rule: {str(e)}")

# Order Management
@app.get("/orders")
async def get_orders():

    try:
        orders_with_ids = []
        for i, order in enumerate(Memory.orders, 1):
            orders_with_ids.append({
                "order_id": i,
                "customer_id": order['customer_id'],
                "product_id": order['product_id'],
                "quantity": order['quantity'],
                "timestamp": "2025-09-29T00:00:00"  # Mock timestamp
            })
        
        return {"orders": orders_with_ids, "total_orders": len(orders_with_ids)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving orders: {str(e)}")

@app.get("/results")
async def get_results():

    try:
        return {"results": Memory.results, "total_results": len(Memory.results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {str(e)}")

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)