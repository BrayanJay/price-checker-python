# GUI for Pricing Engine - FastAPI Integration

This GUI application provides a user-friendly interface to interact with the Pricing Engine FastAPI server. It demonstrates full integration between a Tkinter GUI and RESTful API services.

## Features

### 🎯 System Management
- **API Connection Status**: Real-time connection monitoring with visual indicators
- **Health Checks**: Monitor API server health and system status
- **Data Management**: Load sample data and clear all data with confirmation
- **System Information**: View detailed system status and API responses

### 👥 Customer Management
- **Create Customers**: Add new customers with tiers (SILVER, GOLD, PLATINUM) and groups (REGULAR, BULK, VIP)
- **Customer List**: View all customers with their details in an organized table
- **Customer Search**: Easy access to customer information and loyalty rules count

### 📦 Product Management
- **Create Products**: Add new products with base pricing information
- **Product List**: Browse all products with pricing rule summaries
- **Product Details**: View tier pricing and group pricing rules count

### 💰 Pricing Rules Management
- **Tier Pricing**: Set discount rates based on customer tier levels
- **Group Pricing**: Configure pricing for customer groups (REGULAR, BULK, VIP)
- **Loyalty Pricing**: Create personalized pricing for specific customer-product combinations
- **Minimum Quantity**: Set quantity thresholds for pricing rules

### 🧮 Price Calculator
- **Single Order Calculation**: Calculate final prices for specific customer-product-quantity combinations
- **Price Breakdown**: View detailed calculation results including price type and applied rules
- **Real-time Results**: Instant price calculations with comprehensive result display

### 🔧 API Explorer
- **Custom Requests**: Send GET, POST, and DELETE requests to any endpoint
- **JSON Payload**: Configure request payloads for POST operations
- **Response Viewer**: View formatted API responses with syntax highlighting
- **Endpoint Testing**: Test all available API endpoints with ease

## Quick Start

### Method 1: Using the Launcher (Recommended)
```bash
cd gui
python launcher.py
```

This will automatically:
1. Start the FastAPI server on `http://localhost:8000`
2. Launch the GUI application after a 3-second delay
3. Provide a seamless integrated experience

### Method 2: Manual Setup
1. **Start the API Server** (in terminal 1):
   ```bash
   cd api
   python main.py
   # or
   uvicorn main:app --reload --host localhost --port 8000
   ```

2. **Start the GUI** (in terminal 2):
   ```bash
   cd gui
   python main.py
   ```

## Installation

1. **Install Requirements**:
   ```bash
   cd gui
   pip install -r requirements.txt
   ```

2. **Ensure API Dependencies**:
   ```bash
   cd ../api
   pip install -r requirements.txt
   ```

## GUI Interface Guide

### Navigation Tabs
- **System**: API management, health checks, and data operations
- **Customers**: Create and manage customer accounts with tiers and groups
- **Products**: Add and view products with base pricing
- **Pricing Rules**: Configure tier, group, and loyalty pricing rules
- **Price Calculator**: Calculate final prices for orders
- **API Explorer**: Test and explore all API endpoints

### Status Indicators
- ✅ **Green**: API connected and operational
- ⚠️ **Orange**: API accessible but with errors
- ❌ **Red**: API disconnected or server not running

### Data Flow Examples

1. **Setup Process**:
   - Load sample data → Create customers → Add products → Set pricing rules → Calculate prices

2. **Customer Creation**:
   - Enter customer details → Select tier → Choose groups → Create customer → View in list

3. **Price Calculation**:
   - Select customer → Choose product → Set quantity → Calculate → View detailed results

## API Integration Features

The GUI integrates with all 18 FastAPI endpoints:

### System Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /status` - System status
- `POST /load-sample-data` - Load test data
- `DELETE /clear-data` - Clear all data

### Customer Endpoints
- `GET /customers` - List all customers
- `POST /customers` - Create customer
- `GET /customers/{id}` - Get customer details
- `DELETE /customers/{id}` - Delete customer
- `POST /customers/{id}/loyalty-prices` - Add loyalty pricing

### Product Endpoints
- `GET /products` - List all products
- `POST /products` - Create product
- `GET /products/{id}` - Get product details
- `DELETE /products/{id}` - Delete product
- `POST /products/{id}/tier-prices` - Add tier pricing
- `POST /products/{id}/group-prices` - Add group pricing

### Pricing Endpoints
- `POST /calculate-price` - Calculate single order price
- `POST /calculate-bulk-prices` - Calculate multiple order prices

## Technical Architecture

### GUI Components
- **Main Window**: Tkinter-based with tabbed interface
- **API Client**: HTTP requests using the `requests` library
- **Threading**: Background API status checking
- **Error Handling**: Comprehensive exception handling with user feedback

### Data Models
- **Customer**: ID, name, tier, groups, loyalty rules
- **Product**: ID, name, base price, pricing rules
- **Pricing Rules**: Tier-based, group-based, and loyalty-based pricing
- **Orders**: Customer-product-quantity combinations

### Communication Flow
```
GUI Interface ↔ HTTP Requests ↔ FastAPI Server ↔ Pricing Engine Core
```

## Error Handling

The GUI provides comprehensive error handling:
- **Connection Errors**: Automatic retry with status updates
- **API Errors**: User-friendly error messages with technical details
- **Validation Errors**: Form validation before API submission
- **Timeout Handling**: Configurable timeouts for API requests

## Customization

### Styling
- Modify colors and themes in the `setup_ui()` method
- Adjust window dimensions and layout in `__init__()`

### API Configuration
- Change `self.api_base_url` to point to different server instances
- Modify timeout values in request methods

### Features Extension
- Add new tabs by creating additional `create_*_tab()` methods
- Extend API integration by adding new request methods

## Troubleshooting

### Common Issues

1. **"API Disconnected" Error**:
   - Ensure FastAPI server is running on `http://localhost:8000`
   - Check firewall settings
   - Verify API dependencies are installed

2. **GUI Not Responding**:
   - Check if Python has Tkinter support
   - Ensure `requests` library is installed
   - Verify GUI requirements are met

3. **Data Not Loading**:
   - Click "Load Sample Data" in the System tab
   - Check API server logs for errors
   - Verify API endpoints are accessible

### Performance Tips
- Use "Load Sample Data" for quick testing
- Monitor system status regularly
- Clear data periodically to reset state

This GUI provides a complete demonstration of FastAPI integration with a desktop application, showcasing real-world patterns for API consumption and user interface design.