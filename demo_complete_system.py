from data.memory import Memory
from models.customer import Customer
from models.product import Product
from constants.group import Group
from constants.tier import Tier
from price_calculator import find_best_applicable_price


def demo_complete_system():
    print("=" * 60)
    print("PRICING ENGINE V2 - COMPLETE SYSTEM DEMO")
    print("=" * 60)
    
    # Step 1: Clear and setup
    print("\n1. Initializing system...")
    Memory.clear_all()
    
    # Step 2: Add products with structure [[Product, TierPrices, GroupPrices]]
    print("2. Adding products with pricing rules...")
    
    # Product 1: Laptop with comprehensive pricing
    laptop = Product(1, "Gaming Laptop", 200000)
    laptop_tier_prices = [
        {"product_id": 1, "tier": "GOLD", "discount_rate": 0.15, "min_qty": 2},
        {"product_id": 1, "tier": "SILVER", "discount_rate": 0.08, "min_qty": 3},
        {"product_id": 1, "tier": "PLATINUM", "discount_rate": 0.25, "min_qty": 1}
    ]
    laptop_group_prices = [
        {"product_id": 1, "group": "VIP", "discount_rate": 0.30, "min_qty": 1},
        {"product_id": 1, "group": "BULK", "discount_rate": 0.12, "min_qty": 5},
        {"product_id": 1, "group": "REGULAR", "discount_rate": 0.05, "min_qty": 4}
    ]
    Memory.add_product_with_pricing(laptop, laptop_tier_prices, laptop_group_prices)
    
    # Product 2: Phone
    phone = Product(2, "Smartphone", 80000)
    Memory.add_product_with_pricing(phone)
    
    print(f"   Added {len(Memory.products)} products")
    
    # Step 3: Add customers with structure [[Customer, LoyaltyPrice]]
    print("3. Adding customers with loyalty pricing...")
    
    # Customer 1: VIP Gold customer with loyalty pricing
    alice = Customer(1, "Alice Premium", Tier.GOLD, [Group.VIP, Group.REGULAR])
    alice_loyalty = [
        {"customer_id": 1, "product_id": 1, "discount_rate": 0.20, "min_qty": 1},
        {"customer_id": 1, "product_id": 2, "discount_rate": 0.18, "min_qty": 2}
    ]
    Memory.add_customer_with_loyalty(alice, alice_loyalty)
    
    # Customer 2: Silver bulk customer
    bob = Customer(2, "Bob Business", Tier.SILVER, [Group.BULK])
    Memory.add_customer_with_loyalty(bob)
    
    # Customer 3: Platinum VIP customer
    charlie = Customer(3, "Charlie Elite", Tier.PLATINUM, [Group.VIP])
    Memory.add_customer_with_loyalty(charlie)
    
    print(f"   Added {len(Memory.customers)} customers")
    
    # Step 4: Place various orders
    print("4. Placing test orders...")
    
    test_scenarios = [
        (1, 1, 1, "Alice: 1 Laptop - Should get CUSTOMER loyalty (20% off)"),
        (1, 1, 2, "Alice: 2 Laptops - Should compare CUSTOMER (20%) vs TIER (15%) vs GROUP (30%)"),
        (2, 1, 5, "Bob: 5 Laptops - Should get BULK group discount (12% off)"),
        (3, 1, 1, "Charlie: 1 Laptop - Should get VIP group discount (30% off)"),
        (1, 2, 2, "Alice: 2 Phones - Should get CUSTOMER loyalty (18% off)"),
    ]
    
    for customer_id, product_id, quantity, description in test_scenarios:
        Memory.add_order(customer_id, product_id, quantity)
        print(f"   {description}")
    
    print(f"   Total orders: {len(Memory.orders)}")
    
    # Step 5: Calculate best prices
    print("5. Calculating best applicable prices...")
    
    customers_dict = Memory.get_all_customers()
    products_dict = Memory.get_all_products()
    
    results = find_best_applicable_price(Memory.orders, products_dict, customers_dict)
    
    # Step 6: Store and display results
    print("6. Results:")
    print("-" * 40)
    
    for i, (order, result) in enumerate(zip(Memory.orders, results), 1):
        Memory.add_result(result['product_id'], result['price'], result['price_type'])
        
        customer_data = Memory.get_customer_by_id(order['customer_id'])
        product_data = Memory.get_product_by_id(order['product_id'])
        
        customer_name = customer_data[0].name
        product_name = product_data[0].name
        base_price = product_data[0].base_price
        final_price = result['price']
        savings = base_price - final_price
        savings_pct = (savings / base_price) * 100 if savings > 0 else 0
        
        print(f"Order {i}: {customer_name} - {order['quantity']}x {product_name}")
        print(f"   Base Price: ${base_price:,}")
        print(f"   Final Price: ${final_price:,} ({result['price_type']})")
        print(f"   Savings: ${savings:,} ({savings_pct:.1f}% off)")
        print()
    
    # Step 7: Display memory structure
    print("7. Final Memory Structure:")
    print(f"   Customers: {len(Memory.customers)} entries [[Customer, LoyaltyPrices]]")
    print(f"   Products: {len(Memory.products)} entries [[Product, TierPrices, GroupPrices]]")
    print(f"   Orders: {len(Memory.orders)} entries [dict with customer_id, product_id, quantity]")
    print(f"   Results: {len(Memory.results)} entries [dict with product_id, price, price_type]")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE - System working with enhanced structure!")
    print("=" * 60)


if __name__ == "__main__":
    demo_complete_system()