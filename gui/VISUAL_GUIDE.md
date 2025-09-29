# GUI Visual Guide - Pricing Engine FastAPI Integration

## 🎨 GUI Interface Overview

The Pricing Engine GUI provides a comprehensive interface for managing and interacting with the FastAPI backend. Below is a detailed guide to each component:

### 📋 Main Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🚀 Pricing Engine - FastAPI Integration                                |
├─────────────────────────────────────────────────────────────────────────┤
│ ✅ API Connected - Ready                ⚠️ DEMO MODE - Using mock data │
├─────────────────────────────────────────────────────────────────────────┤
│ [📊 Overview] [👥 Customers] [📦 Products] [💰 Pricing Rules]         |
| [🧮 Calculator] [🔧 API Explorer] │                                    |
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                        TAB CONTENT AREA                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 🎯 Tab-by-Tab Interface Guide

#### 1. 📊 System/Overview Tab
```
┌─ System Management ─────────────────────────────────────────────────────┐
│ [Check Health] [Get Status] [Refresh Connection]                        │
├─ Data Management ───────────────────────────────────────────────────────┤
│ [Load Sample Data] [Clear All Data]                                     │
├─ System Information ────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ System Status:                                                      │ │
│ │ Status: 200                                                         │ │
│ │ Response: {"status": "healthy", "customers": 3, "products": 5}      │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2. 👥 Customers Tab
```
┌─ Create Customer ───────────────────────────────────────────────────────┐
│ Customer ID: [____] Name: [________________] Tier: [GOLD ▼]             │
│ Groups: ☑ REGULAR ☐ BULK ☑ VIP                                         │
│ [Create Customer] [Load Customers] [Clear Form]                         │
├─ Customer List ─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ID │ Name      │ Tier     │ Groups        │ Loyalty Rules │         │ │
│ │ 1  │ John Doe  │ GOLD     │ REGULAR, VIP  │ 2            │          │ │
│ │ 2  │ Jane Smith│ PLATINUM │ BULK          │ 1            │          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3. 📦 Products Tab
```
┌─ Create Product ────────────────────────────────────────────────────────┐
│ Product ID: [____] Name: [________________] Base Price: [______]         │
│ [Create Product] [Load Products] [Clear Form]                           │
├─ Product List ──────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ID  │ Name           │ Base Price │ Tier Rules │ Group Rules │      │ │
│ │ 101 │ Premium Widget │ $99.99     │ 3          │ 2           │      │ │
│ │ 102 │ Standard Widget│ $49.99     │ 2          │ 1           │      │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 4. 💰 Pricing Rules Tab
```
┌─ Add Tier Pricing Rule ─────────────────────────────────────────────────┐
│ Product ID: [___] Tier: [GOLD ▼] Discount: [___] Min Qty: [___]         │
│                      [Add Tier Rule]                                    │
├─ Add Group Pricing Rule ────────────────────────────────────────────────┤
│ Product ID: [___] Group: [VIP ▼] Discount: [___] Min Qty: [___]         │
│                      [Add Group Rule]                                   │
├─ Add Loyalty Pricing Rule ──────────────────────────────────────────────┤
│ Customer ID: [___] Product ID: [___] Discount: [___] Min Qty: [___]     │
│                      [Add Loyalty Rule]                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5. 🧮 Price Calculator Tab
```
┌─ Single Price Calculation ──────────────────────────────────────────────┐
│ Customer ID: [___] Product ID: [___] Quantity: [___]                    │
│                    [Calculate Price]                                    │
├─ Calculation Results ───────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Price Calculation Result:                                           │ │
│ │ ========================                                            │ │
│ │ Customer ID: 1                                                      │ │
│ │ Product ID: 101                                                     │ │
│ │ Quantity: 5                                                         │ │
│ │                                                                     │ │
│ │ Result:                                                             │ │
│ │ - Product: 101                                                      │ │
│ │ - Final Price: $449.95                                              │ │
│ │ - Price Type: tier_pricing                                          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 6. 🔧 API Explorer Tab
```
┌─ API Request ───────────────────────────────────────────────────────────┐
│ Method: [GET ▼] Endpoint: [/status        ▼] [Send Request]            │
├─ JSON Payload (for POST requests) ──────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ {                                                                   │ │
│ │   "example": "payload"                                              │ │
│ │ }                                                                   │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
├─ API Response ──────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Request: GET http://localhost:8000/status                           │ │
│ │ Status Code: 200                                                    │ │
│ │ Response:                                                           │ │
│ │ {                                                                   │ │
│ │   "status": "healthy",                                              │ │
│ │   "customers": 3,                                                   │ │
│ │   "products": 5                                                     │ │
│ │ }                                                                   │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎨 Visual Design Elements

### Color Scheme
- **Header**: Dark blue (#2c3e50) with white text
- **Status Indicators**: 
  - Green (✅): Connected/Success
  - Orange (⚠️): Warning/Demo mode
  - Red (❌): Error/Disconnected
- **Background**: Light gray (#f0f0f0)
- **Buttons**: Standard system buttons with hover effects

### Interactive Elements
- **Combo Boxes**: Dropdown selections for tiers, groups, methods
- **Entry Fields**: Text input with validation feedback
- **Check Boxes**: Multi-select for customer groups
- **Tree Views**: Sortable tables for data display
- **Scrolled Text**: Results display with syntax highlighting
- **Buttons**: Action buttons with descriptive labels

### Status Indicators
```
Connection Status Bar:
┌─────────────────────────────────────────────────────────────────────────┐
│ ✅ API Connected - Ready                    ⚠️ DEMO MODE - Using mock data │
└─────────────────────────────────────────────────────────────────────────┘

Status Messages:
• ✅ API Connected - Ready (Green)
• ⚠️ API Error - Check server (Orange) 
• ❌ API Disconnected - Start server (Red)
• 🔄 Checking API connection... (Blue)
```

## 🔄 User Workflow Examples

### Typical User Journey
1. **Start Application** → Check API status
2. **Load Sample Data** → Populate with test data
3. **Browse Customers** → View existing customers
4. **Browse Products** → View available products
5. **Create Pricing Rules** → Set up tier/group/loyalty pricing
6. **Calculate Prices** → Test pricing scenarios
7. **Use API Explorer** → Test custom endpoints

### Demo Mode Journey
1. **Start Demo** → Automatic mock data loading
2. **Explore Interface** → Navigate through tabs
3. **Create Test Data** → Add customers/products
4. **Run Calculations** → See realistic pricing
5. **Learn API Integration** → Understand patterns

## 📱 Responsive Design Features

- **Resizable Windows**: All components scale properly
- **Scrollable Content**: Large data sets handled gracefully
- **Tab Navigation**: Easy switching between features
- **Keyboard Shortcuts**: Standard navigation support
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during operations

## 🎯 Integration Highlights

The GUI demonstrates these FastAPI integration patterns:

1. **HTTP Client**: Using `requests` library for API calls
2. **Async Operations**: Threading for non-blocking API calls
3. **Error Handling**: Comprehensive exception management
4. **Data Validation**: Form validation before API submission
5. **Real-time Updates**: Live status monitoring
6. **JSON Serialization**: Proper data formatting
7. **Response Processing**: Parsing and displaying API responses
8. **Authentication Ready**: Framework for token-based auth
9. **Configuration Management**: Flexible API endpoint configuration
10. **Performance Monitoring**: Connection status and health checks

This GUI serves as a complete example of how to build desktop applications that integrate seamlessly with FastAPI backends, providing both functionality and user experience best practices.