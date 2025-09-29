# FastAPI Pricing Engine

This directory contains the FastAPI implementation of the Pricing Engine.

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

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check |
| GET | `/status` | System status and data counts |

### Data Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/load-sample-data` | Load sample customers, products, and pricing rules |
| GET | `/customers` | Get all customers with their information |
| GET | `/products` | Get all products with their information |
| DELETE | `/clear-data` | Clear all data from memory |

### Price Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/calculate-price` | Calculate best price for a single order |
| POST | `/calculate-bulk-prices` | Calculate best prices for multiple orders |

## Request/Response Examples

### Single Price Calculation

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
    "price": 175000,
    "price_type": "GROUP"
}
```

### Bulk Price Calculation

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
        {"product_id": "P001", "price": 175000, "price_type": "GROUP"},
        {"product_id": "P001", "price": 315000, "price_type": "GROUP"},
        {"product_id": "P001", "price": 175000, "price_type": "GROUP"}
    ],
    "total_orders": 3
}
```

## Testing

Run the test script to verify all endpoints:

```bash
# Make sure the API server is running first
python api/test_api.py
```

## Sample Data

The API includes sample data with:
- **3 Customers**: Alice (GOLD/BULK/VIP), Bob (SILVER/BULK), Charlie (PLATINUM/VIP)
- **3 Products**: Gaming Laptop (₹350,000), Smartphone (₹200,000), Tablet (₹150,000)
- **Pricing Rules**: Tier discounts, group discounts, and loyalty pricing

## Price Types

- **BASE**: Product base price (no discount)
- **TIER**: Tier-based discount (GOLD, SILVER, PLATINUM)
- **GROUP**: Group-based discount (VIP, BULK, REGULAR)
- **CUSTOMER**: Customer-specific loyalty discount

## Error Handling

The API includes comprehensive error handling:
- 400: Bad Request (invalid input, missing data)
- 404: Not Found (invalid customer/product IDs)
- 500: Internal Server Error (system errors)

All errors return detailed error messages in JSON format.