import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.memory import Memory
from models.customer import Customer
from models.product import Product
from constants.group import Group
from constants.tier import Tier
from price_calculator import find_best_applicable_price

class Main:

    @staticmethod
    def run():
        while True:
            print("Welcome to Pricing Engine v2")
            print("="*50)
            print("Menu")
            print("1. Add Product")
            print("2. Add Customer")
            print("3. View Products")
            print("4. View Customers")
            print("5. Add Tier Pricing Rule")
            print("6. Add Group Pricing Rule")
            print("7. Place Order")
            print("8. Add Loyalty Price")
            print("9. View Orders")
            print("10. Calculate Best Applicable Price")
            print("11. View Results")
            print("12. Load Sample Data")
            print("13. Clear All Data")
            print("0. Exit")

            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == '0':
                    print("Exiting the application. Goodbye!")
                    break

                elif choice == '1':
                    Main.add_product()

                elif choice == '2':
                    Main.add_customer()

                elif choice == '3':
                    Memory.view_products()

                elif choice == '4':
                    Memory.view_customers()

                elif choice == '5':
                    Main.add_tier_pricing_rule()

                elif choice == '6':
                    Main.add_group_pricing_rule()

                elif choice == '7':
                    Main.place_order()

                elif choice == '8':
                    Main.add_loyalty_price()

                elif choice == '9':
                    Memory.view_orders()

                elif choice == '10':
                    Main.calculate_best_prices()

                elif choice == '11':
                    Memory.view_results()

                elif choice == '12':
                    Main.load_sample_data()

                elif choice == '13':
                    Memory.clear_all()

                else:
                    print("Invalid choice. Please try again.")

            except Exception as e:
                print(f"Error: {e}")
                print("Please try again.")

    @staticmethod
    def add_product():
        try:
            print("Existing Products:")
            for product in Memory.get_all_products():
                print(f"Product ID: {product.product_id} | Name: {product.name} | Base Price: {product.base_price} | Tier Prices: {len(product.tier_prices)} | Group Prices: {len(product.group_prices)}")
            
            print("\n--- Add New Product ---")
            product_id = int(input("Enter product ID (hint: integers only): "))
            
            # Check if product already exists
            if Memory.get_product_by_id(product_id):
                print(f"Product with ID {product_id} is already exists!")
                return
            
            name = input("Enter product name: ")
            base_price = float(input("Enter base price: "))
            
            product = Product(product_id=product_id, name=name, base_price=base_price)
            Memory.add_product_with_pricing(product)
            
            print(f"Product '{name}' added successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers for Product ID and Base Price.")
        except Exception as e:
            print(f"Error adding product: {e}")

    @staticmethod
    def add_customer():
        
        try:
            print("\n--- Add Customer ---")
            customer_id = int(input("Enter customer ID (hint: integers only): "))
            
            # Check if customer already exists
            if Memory.get_customer_by_id(customer_id):
                print(f"Customer with ID {customer_id} is already exists!")
                return
            
            name = input("Enter customer name: ")
            
            # Select tier
            print("Available tiers:")
            for tier in Tier:
                print(f"  {tier.value}")
            tier_input = input("Enter customer tier (Eg:-Silver): ").upper()
            
            # Find the matching tier enum
            tier = None
            for t in Tier:
                if t.value.lower() == tier_input.lower():
                    tier = t
                    break
            
            if tier is None:
                print(f"Invalid tier '{tier_input}'. Available tiers: {', '.join([t.value for t in Tier])}")
                return
            
            # Select groups
            print("Available groups:")
            for group in Group:
                print(f"  {group.value}")
            
            groups = []
            while True:
                group_input = input("Enter a group name or 'done' to complete Customer Creation: ").strip()
                if group_input.lower() == 'done':
                    break
                
                # Find matching group
                group = None
                for g in Group:
                    if g.value.lower() == group_input.lower():
                        group = g
                        break
                
                if group is None:
                    print(f"Invalid group '{group_input}'. Available groups: {', '.join([g.value for g in Group])}")
                    continue
                
                if group not in groups:
                    groups.append(group)
                    print(f"Group added successfully! \n Group: {group.value}")
                else:
                    print("Group already added!")
            
            customer = Customer(customer_id=customer_id, name=name, tier=tier, groups=groups)
            Memory.add_customer_with_loyalty(customer)

            print(f"Customer with name '{name}' added successfully!")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding customer: {e}")

    @staticmethod
    def add_tier_pricing_rule():
        try:
            print("\n--- Add Tier Prices ---")

            print("Available Products:")
            Memory.view_products()
            
            product_id = int(input("Enter product ID: "))
            product_data = Memory.get_product_by_id(product_id)
            
            if not product_data:
                print("Product not found!")
                return
            
            product, tier_prices, group_prices = product_data
            
            print("Available tiers:")
            for tier in Tier:
                print(f"  {tier.value}")

            tier_input = input("Enter tier (Silver, Gold or Platinum): ").strip()
            tier = None
            for t in Tier:
                if t.value.lower() == tier_input.lower():
                    tier = t
                    break
            
            if tier is None:
                print(f"Invalid tier '{tier_input}'. Available tiers: {', '.join([t.value for t in Tier])}")
                return
            
            discount_rate = float(input("Enter discount rate (0.0 to 1.0): "))
            min_qty = int(input("Enter minimum quantity: "))
            
            # Check if tier rule already exists
            for tp in tier_prices:
                if tp['tier'] == tier.value:
                    print(f"Tier pricing rule for {tier.value} already exists!")
                    return
            
            tier_rule = {
                "product_id": product_id,
                "tier": tier.value,
                "discount_rate": discount_rate,
                "min_qty": min_qty
            }
            
            tier_prices.append(tier_rule)
            print(f"Tier pricing rule added for {tier.value}!")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding tier pricing rule: {e}")

    @staticmethod
    def add_group_pricing_rule():
        try:
            print("\n--- Add Group Pricing ---")
            Memory.view_products()
            
            product_id = int(input("Enter product ID: "))
            product_data = Memory.get_product_by_id(product_id)
            
            if not product_data:
                print("Product not found!")
                return
            
            product, tier_prices, group_prices = product_data
            
            print("Available groups:")
            for group in Group:
                print(f"  {group.value}")
            
            group_input = input("Enter group: ").strip()
            group = None
            for g in Group:
                if g.value.lower() == group_input.lower():
                    group = g
                    break
            
            if group is None:
                print(f"Invalid group '{group_input}'. Available groups: {', '.join([g.value for g in Group])}")
                return
            
            discount_rate = float(input("Enter discount rate (0.0 to 1.0): "))
            min_qty = int(input("Enter minimum quantity: "))
            
            # Check if group rule already exists
            for gp in group_prices:
                if gp['group'] == group.value:
                    print(f"Group pricing rule for {group.value} already exists!")
                    return
            
            group_rule = {
                "product_id": product_id,
                "group": group.value,
                "discount_rate": discount_rate,
                "min_qty": min_qty
            }
            
            group_prices.append(group_rule)
            print(f"Group pricing rule added for {group.value}!")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding group pricing rule: {e}")

    @staticmethod
    def place_order():
        try:
            print("\n--- Place Order ---")
            Memory.view_customers()
            customer_id = int(input("Enter customer ID: "))
            
            Memory.view_products()
            product_id = int(input("Enter product ID: "))
            
            quantity = int(input("Enter quantity: "))
            
            # Validate customer and product exist
            if not Memory.get_customer_by_id(customer_id):
                print("Customer not found!")
                return
            
            if not Memory.get_product_by_id(product_id):
                print("Product not found!")
                return
            
            Memory.add_order(customer_id, product_id, quantity)
            print("Order placed successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"Error placing order: {e}")

    @staticmethod
    def add_loyalty_price():
        try:
            print("\n--- Add Loyalty Price ---")
            Memory.view_customers()
            customer_id = int(input("Enter customer ID: "))
            
            customer_data = Memory.get_customer_by_id(customer_id)
            if not customer_data:
                print("Customer not found!")
                return
            
            customer, loyalty_prices = customer_data
            
            Memory.view_products()
            product_id = int(input("Enter product ID: "))
            
            if not Memory.get_product_by_id(product_id):
                print("Product not found!")
                return
            
            # Check if loyalty rule already exists
            for lp in loyalty_prices:
                if lp['product_id'] == product_id:
                    print(f"Loyalty pricing for product {product_id} already exists!")
                    return
            
            discount_rate = float(input("Enter discount rate (0.0 to 1.0): "))
            min_qty = int(input("Enter minimum quantity: "))
            
            loyalty_rule = {
                "customer_id": customer_id,
                "product_id": product_id,
                "discount_rate": discount_rate,
                "min_qty": min_qty
            }
            
            loyalty_prices.append(loyalty_rule)
            print("Loyalty pricing rule added successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"Error adding loyalty price: {e}")

    @staticmethod
    def calculate_best_prices():
        try:
            print("\n--- Calculate Best Applicable Prices ---")
            
            if not Memory.orders:
                print("No orders found. Please place some orders first.")
                return
            
            # Get data in dictionary format for price calculator
            customers_dict = Memory.get_all_customers()
            products_dict = Memory.get_all_products()
            
            # Calculate best prices
            results = find_best_applicable_price(Memory.orders, products_dict, customers_dict)
            
            # Store results and display
            Memory.results.clear()  # Clear previous results
            
            print("\nCalculation Results:")
            print("-" * 60)
            for i, result in enumerate(results, 1):
                Memory.add_result(result['product_id'], result['price'], result['price_type'])
                print(f"{i}. Product {result['product_id']}: LKR {result['price']} ({result['price_type']})")
            
            print(f"\nCalculated prices for {len(results)} orders.")
            print("Results stored in memory.")
            
        except Exception as e:
            print(f"Error calculating prices: {e}")

    @staticmethod
    def load_sample_data():
        try:
            print("\n--- Loading Sample Data ---")
            
            # Clear existing data
            Memory.clear_all()
            
            # Add sample products
            product1 = Product(1, "Laptop", 350000)
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
            customer1 = Customer(1, "Alice", Tier.GOLD, [Group.BULK, Group.VIP])
            customer2 = Customer(2, "Bob", Tier.SILVER, [Group.BULK])
            customer3 = Customer(3, "Charlie", Tier.PLATINUM, [Group.VIP])
            
            # Add customers with loyalty pricing
            loyalty_prices_c1 = [
                {"customer_id": 1, "product_id": 2, "discount_rate": 0.20, "min_qty": 5},
                {"customer_id": 1, "product_id": 1, "discount_rate": 0.10, "min_qty": 10},
                {"customer_id": 1, "product_id": 3, "discount_rate": 0.50, "min_qty": 2}
            ]
            
            Memory.add_customer_with_loyalty(customer1, loyalty_prices_c1)
            Memory.add_customer_with_loyalty(customer2)
            Memory.add_customer_with_loyalty(customer3)
            
            # Add sample orders
            Memory.add_order(1, 1, 5)   # Alice orders 5 Laptops
            Memory.add_order(2, 1, 10)  # Bob orders 10 Laptops
            Memory.add_order(1, 2, 3)   # Alice orders 3 Smartphones
            
            print("Sample data loaded successfully!")
            print("- 3 Products with pricing rules")
            print("- 3 Customers with loyalty pricing")
            print("- 3 Sample orders")
            
        except Exception as e:
            print(f"Error loading sample data: {e}")


if __name__ == "__main__":
    Main.run()