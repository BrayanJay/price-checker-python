# FastAPI Pricing Engine - RESTful Edition

This directory contains the complete FastAPI implementation of the Pricing Engine with full CRUD operations and RESTful API design.

## Features

✅ **Complete RESTful API** with 18 endpoints  
✅ **Full CRUD Operations** for customers and products  
✅ **Dynamic Pricing Rules Management** (Tier, Group, Loyalty)  
✅ **Bulk Price Calculations** with validation  
✅ **Comprehensive Error Handling** (400, 404, 500)  
✅ **Auto-generated Documentation** (OpenAPI/Swagger)  
✅ **Request/Response Validation** with Pydantic  
✅ **Order Tracking** and result history  

## Setup

1. Install dependencies:
```bash
pip install -r api/requirements.txt
```

2. Run the API server:
```bash
# Option 1: Using uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python api/main.py
```

3. Access the API:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Information**: http://localhost:8000/

## API Endpoints (18 Total)

### System Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check |
| GET | `/status` | System status and data counts |
| POST | `/load-sample-data` | Load sample customers, products, and pricing rules |
| DELETE | `/clear-data` | Clear all data from memory |

### Customer Management (CRUD)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List all customers with their information |
| GET | `/customers/{customer_id}` | Get specific customer by ID |
| POST | `/customers` | Create a new customer |
| DELETE | `/customers/{customer_id}` | Delete customer by ID |
| POST | `/customers/{customer_id}/loyalty-prices` | Add loyalty pricing rule to customer |

### Product Management (CRUD)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products with their information |
| GET | `/products/{product_id}` | Get specific product by ID |
| POST | `/products` | Create a new product |
| DELETE | `/products/{product_id}` | Delete product by ID |
| POST | `/products/{product_id}/tier-prices` | Add tier-based pricing rule to product |
| POST | `/products/{product_id}/group-prices` | Add group-based pricing rule to product |

### Price Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/calculate-price` | Calculate best price for a single order |
| POST | `/calculate-bulk-prices` | Calculate best prices for multiple orders |

### Order & Results Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | Get all order history |
| GET | `/results` | Get all calculation results |

## Request/Response Examples

### 1. Create Customer

**Request:**
```json
POST /customers
{
    "customer_id": 1,
    "name": "John Doe",
    "tier": "GOLD",
    "groups": ["VIP", "BULK"]
}
```

**Response:**
```json
{
    "customer_id": 1,
    "name": "John Doe",
    "tier": "Gold",
    "groups": ["VIP", "Bulk"],
    "loyalty_products_count": 0
}
```

### 2. Create Product

**Request:**
```json
POST /products
{
    "product_id": 1,
    "name": "Gaming Laptop",
    "base_price": 350000
}
```

**Response:**
```json
{
    "product_id": 1,
    "name": "Gaming Laptop",
    "base_price": 350000,
    "tier_prices_count": 0,
    "group_prices_count": 0
}
```

### 3. Add Tier Pricing Rule

**Request:**
```json
POST /products/1/tier-prices
{
    "product_id": 1,
    "tier": "GOLD",
    "discount_rate": 0.15,
    "min_qty": 2
}
```

**Response:**
```json
{
    "message": "Tier pricing rule added for Gold"
}
```

### 4. Add Loyalty Pricing

**Request:**
```json
POST /customers/1/loyalty-prices
{
    "customer_id": 1,
    "product_id": 1,
    "discount_rate": 0.20,
    "min_qty": 1
}
```

**Response:**
```json
{
    "message": "Loyalty pricing rule added for product 1"
}
```

### 5. Single Price Calculation

**Request:**
```json
POST /calculate-price
{
    "customer_id": 1,
    "product_id": 1,
    "quantity": 5
}
```

**Response:**
```json
{
    "product_id": "P001",
    "price": 280000,
    "price_type": "CUSTOMER"
}
```

### 6. Bulk Price Calculation

**Request:**
```json
POST /calculate-bulk-prices
{
    "orders": [
        {"customer_id": 1, "product_id": 1, "quantity": 2},
        {"customer_id": 2, "product_id": 1, "quantity": 10},
        {"customer_id": 3, "product_id": 1, "quantity": 1}
    ]
}
```

**Response:**
```json
{
    "results": [
        {"product_id": "P001", "price": 280000, "price_type": "CUSTOMER"},
        {"product_id": "P001", "price": 315000, "price_type": "GROUP"},
        {"product_id": "P001", "price": 175000, "price_type": "GROUP"}
    ],
    "total_orders": 3
}
```

### 7. Get Customer Details

**Request:**
```http
GET /customers/1
```

**Response:**
```json
{
    "customer_id": 1,
    "name": "John Doe",
    "tier": "Gold",
    "groups": ["VIP", "Bulk"],
    "loyalty_products_count": 1
}
```

## Quick Start Guide

### 1. Load Sample Data
```bash
curl -X POST http://localhost:8000/load-sample-data
```

### 2. View Available Customers
```bash
curl -X GET http://localhost:8000/customers
```

### 3. View Available Products
```bash
curl -X GET http://localhost:8000/products
```

### 4. Calculate a Price
```bash
curl -X POST http://localhost:8000/calculate-price \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "product_id": 1, "quantity": 5}'
```

### 5. View System Status
```bash
curl -X GET http://localhost:8000/status
```

## Testing

Run the comprehensive test script to verify all endpoints:

```bash
# Make sure the API server is running first
python api/test_api.py
```

## Data Models

### Customer Tiers
- **SILVER**: Basic tier with standard discounts
- **GOLD**: Premium tier with enhanced discounts  
- **PLATINUM**: Elite tier with maximum discounts

### Customer Groups
- **REGULAR**: Standard customer group
- **BULK**: Volume purchase customers
- **VIP**: Premium service customers

### Price Types (Result Indicators)
- **NORMAL**: Product base price (no discount applied)
- **TIER**: Tier-based discount (SILVER/GOLD/PLATINUM)
- **GROUP**: Group-based discount (REGULAR/BULK/VIP)
- **CUSTOMER**: Customer-specific loyalty discount

## Sample Data

The API includes comprehensive sample data with:
- **3 Customers**: Alice Premium (GOLD/BULK/VIP), Bob Business (SILVER/BULK), Charlie Elite (PLATINUM/VIP)
- **3 Products**: Gaming Laptop (₹350,000), Smartphone (₹200,000), Tablet (₹150,000)
- **Multiple Pricing Rules**: Tier discounts, group discounts, and loyalty pricing
- **Realistic Scenarios**: Various discount combinations and minimum quantities

## Pricing Logic

The system follows a **best price strategy**:

1. **Calculate all applicable prices:**
   - Base price (always available)
   - Tier discount (if customer tier qualifies and min quantity met)
   - Group discount(s) (if customer belongs to group(s) and min quantity met)
   - Loyalty discount (if customer has specific product discount and min quantity met)

2. **Select the lowest price** among all applicable options

3. **Return the result** with price type indicator

## Error Handling

The API includes comprehensive error handling with proper HTTP status codes:

- **200**: Success - Request completed successfully
- **201**: Created - Resource created successfully  
- **400**: Bad Request - Invalid input, validation errors, duplicate resources
- **404**: Not Found - Customer/Product ID not found
- **500**: Internal Server Error - System errors, calculation failures

### Error Response Format
```json
{
    "detail": "Descriptive error message explaining what went wrong"
}
```

## API Documentation

The API provides auto-generated documentation:
- **Swagger UI**: http://localhost:8000/docs (Interactive documentation)
- **ReDoc**: http://localhost:8000/redoc (Alternative documentation format)
- **OpenAPI Schema**: http://localhost:8000/openapi.json (Machine-readable schema)

## Production Considerations

For production deployment, consider:
- Add authentication/authorization
- Implement rate limiting
- Add persistent database storage
- Configure CORS policies
- Set up logging and monitoring
- Add input sanitization
- Implement data backup strategies