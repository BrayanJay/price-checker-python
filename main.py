class Main:

    def run():
        while True:

            print("Welcome to Pricing Engine v2")
            print("Menu")
            print("1. Add Product")
            print("2. Add Customer")
            print("3. View Products")
            print("4. View Customers")
            print("5. View Pricing Rules")
            print("6. Place Order")
            print("7. Add Loyalty Price")
            print("8. View Loyalty Prices")
            print("9. Calculate Best Applicable Price")
            print("0. Exit")


            choice = int(input("Enter your choice: "))
            if choice == '0':
                print("Exiting the application.")
                break

            elif choice == 1:
                from models.product import Product

                Product.add_product()

            elif choice == 2:
                from models.customer import Customer

                Customer.add_customer()

            elif choice == 3:
                from models.product import Product

                Product.view_products()

            elif choice == 4:
                from models.customer import Customer

                Customer.view_customers()

            elif choice == 5:
                from models.pricing_rule import PricingRule

                PricingRule.sub_menu()

            elif choice == 6:
                from models.place_order import PlaceOrder

                PlaceOrder.add_order()

            elif choice == 7:
                from price_hierarchy.loyalty_prices import LoyaltyPrices

                customer_id = input("Enter customer ID: ")
                product_id = input("Enter product ID: ")
                discount_rate = input("Enter discount rate: ")
                LoyaltyPrices.add_loyalty_price(customer_id, product_id, discount_rate)

            elif choice == 8:
                from price_hierarchy.loyalty_prices import LoyaltyPrices

                loyalty_prices = LoyaltyPrices.get_loyalty_prices()
                if not loyalty_prices:
                    print("No loyalty prices available.")
                else:
                    for record in loyalty_prices:
                        print(f"Customer ID: {record['customer_id']}, Product ID: {record['product_id']}, Discount Rate: {record['discount_rate']}")

            elif choice == 9:
                pass

            
            else:
                print("Invalid choice. Please try again.")

    run()