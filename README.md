# Pricing Engine v2 - Enhanced System Guide

## Overview
The enhanced pricing engine stores data in memory with the following structure:

### Memory Structure
```python
customers = [[Customer, LoyaltyPrices]]      # Customer objects with loyalty pricing rules
products = [[Product, TierPrices, GroupPrices]]  # Product objects with tier and group pricing rules  
orders = [{"customer_id": , "product_id": , "quantity": }]  # Order dictionaries
results = [{"product_id": , "price":, "price_type"}]        # Calculation results
```

## Usage

### 1. Running the Application
```bash
python main.py
```

### 2. Menu Options

**Setup Data:**
- **Option 1**: Add Product - Creates new products
- **Option 2**: Add Customer - Creates new customers with tier and groups
- **Option 5**: Add Tier Pricing Rule - Add tier-based discounts to products
- **Option 6**: Add Group Pricing Rule - Add group-based discounts to products
- **Option 8**: Add Loyalty Price - Add customer-specific loyalty pricing

**Operations:**
- **Option 7**: Place Order - Create new orders
- **Option 10**: Calculate Best Applicable Price - Calculate optimal prices for all orders

**View Data:**
- **Option 3**: View Products - Show all products with pricing rules
- **Option 4**: View Customers - Show all customers with loyalty pricing
- **Option 9**: View Orders - Show all placed orders
- **Option 11**: View Results - Show calculation results

**Utilities:**
- **Option 12**: Load Sample Data - Load test data for demonstration
- **Option 13**: Clear All Data - Reset the system

### 3. Data Flow

1. **Add Products** with base prices
2. **Add Customers** with tiers (GOLD, SILVER, PLATINUM) and groups (VIP, BULK, REGULAR)
3. **Set up pricing rules:**
   - Tier pricing: Discounts based on customer tier
   - Group pricing: Discounts based on customer group membership
   - Loyalty pricing: Customer-specific discounts
4. **Place Orders** specifying customer, product, and quantity
5. **Calculate Prices** - System finds the best (lowest) applicable price among:
   - BASE: Product base price
   - TIER: Tier-based discount
   - GROUP: Group-based discount  
   - CUSTOMER: Loyalty/customer-specific discount

### 4. Price Calculation Logic

The system evaluates all applicable pricing rules and selects the lowest price:

- **Tier Pricing**: Based on customer's tier level and minimum quantity
- **Group Pricing**: Based on customer's group memberships and minimum quantity
- **Loyalty Pricing**: Customer-specific discounts with minimum quantity requirements
- **Base Pricing**: Fallback to product's base price

### 5. Example Flow

```
1. Add Product: "Laptop", LKR 100,000 base price
2. Add Tier Rule: GOLD customers get 15% off with min qty 2
3. Add Group Rule: VIP customers get 25% off with min qty 1
4. Add Customer: "Alice", GOLD tier, VIP group
5. Add Loyalty Rule: Alice gets 20% off laptops with min qty 1
6. Place Order: Alice orders 1 Laptop
7. Calculate: System compares:
   - Base: LKR 100,000
   - Tier: LKR 85,000 (15% off, but needs qty 2 - not applicable)
   - Group: LKR 75,000 (25% off VIP discount)
   - Loyalty: LKR 80,000 (20% off customer-specific)
   - Result: LKR 75,000 (GROUP) - best price
```

### 6. Constants Usage

The system uses constants for data mapping:
- **Tier**: `GOLD`, `SILVER`, `PLATINUM` 
- **Group**: `VIP`, `BULK`, `REGULAR`
- **Price Types**: `BASE`, `TIER`, `GROUP`, `CUSTOMER`

### 7. Memory Integration

All user inputs are automatically stored in the memory structure:
- Customer objects with loyalty pricing rules
- Product objects with tier and group pricing rules
- Order dictionaries for tracking purchases
- Result dictionaries for storing calculated prices

### 8. Design Principles and Decisions

The system was built following several key design principles with specific reasoning:

#### **8.1 Memory Structure Design**
**Decision**: Use nested list structure `[[Object, Rules]]` instead of separate storage
**Reasoning**: 
- **Data Cohesion**: Keeps related data together (customer with their loyalty prices, product with their pricing rules)
- **Performance**: Single lookup retrieves both entity and its associated rules
- **Maintainability**: Easier to manage relationships and ensure data consistency
- **Scalability**: Simple to extend with additional rule types without restructuring

#### **8.2 Dictionary-Based Data Exchange**
**Decision**: Convert objects to dictionaries for price calculation functions
**Reasoning**:
- **Separation of Concerns**: Business logic (price calculation) separated from data storage
- **Flexibility**: Price calculator can work with any data source (database, API, files)
- **Testing**: Easier to create test data without complex object initialization
- **Future-Proofing**: Can easily integrate with external systems or different data formats

#### **8.3 Constants Usage for Enums**
**Decision**: Use Python Enums for Tier, Group, and Price Type constants
**Reasoning**:
- **Type Safety**: Prevents invalid values and typos
- **Code Clarity**: Self-documenting code with clear valid options
- **Maintainability**: Single source of truth for valid values
- **IDE Support**: Auto-completion and validation in development tools

#### **8.4 Modular Architecture**
**Decision**: Separate modules for models, pricing logic, memory, and UI
**Reasoning**:
- **Single Responsibility**: Each module has one clear purpose
- **Reusability**: Price calculator can be used independently
- **Testing**: Individual components can be tested in isolation
- **Maintenance**: Changes in one area don't affect others

#### **8.5 Best Price Selection Strategy**
**Decision**: Always select the lowest applicable price among all discount types
**Reasoning**:
- **Customer Benefit**: Ensures customers always get the best deal
- **Business Logic**: Transparent and fair pricing model
- **Competitive Advantage**: Builds customer trust and loyalty
- **Simplicity**: Clear rule that's easy to understand and implement

#### **8.6 Minimum Quantity Requirements**
**Decision**: Each discount rule has minimum quantity thresholds
**Reasoning**:
- **Business Control**: Allows fine-tuning of discount eligibility
- **Volume Incentives**: Encourages larger purchases
- **Profitability**: Protects margins on small orders
- **Flexibility**: Different rules can have different thresholds

#### **8.7 Error Handling and Validation**
**Decision**: Comprehensive input validation and graceful error handling
**Reasoning**:
- **User Experience**: Prevents crashes and provides helpful feedback
- **Data Integrity**: Ensures only valid data enters the system
- **Robustness**: System continues working even with invalid inputs
- **Debugging**: Clear error messages help identify issues quickly

#### **8.8 Interactive Menu System**
**Decision**: Console-based menu instead of GUI or web interface
**Reasoning**:
- **Simplicity**: Easy to implement and test
- **Universal**: Works on any system with Python
- **Focus**: Emphasizes business logic over presentation
- **Development Speed**: Faster to build and iterate

The enhanced system provides a complete pricing engine with flexible discount rules and automatic best-price calculation.