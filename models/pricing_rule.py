from constants.tier import Tier
from constants.group import Group

class PricingRule:

    def tier_pricing_rules(tier: Tier):
        print(f"{tier} calculation")
        print(f"Final Price per product = Base price of a product * {tier} discount rate")
        print("NOTE: This price is only applicable when the minimum quantity of the product is matched.")

        print(f"Eg:- \nProduct Details \n\n product_id: 01 \n product_name: Laptop \n base_price: LKR 350000")
        print(f"Eg:- \nTier Discount Details \n\n {tier}: 0.10 (10%)")
        print(f"Eg:- \nCustomer Details \n\n customer_id: 01 \n customer_name: John Doe \n customer_tier: {tier}")

        print(f"Final price of the Laptop \n = 350000*(1-0.15) \n = 350000*0.85 \n = 297500")
        print(f"\n {"="*100} \n")

    def group_pricing_rules(group: Group):
        print(f"{group} calculation")
        print(f"Final Price per product = Base price of a product * {group} discount rate")
        print("NOTE: This price is only applicable when the minimum quantity of the product is matched.")

        print(f"Eg:- \nProduct Details \n\n product_id: 01 \n product_name: Laptop \n base_price: LKR 350000")
        print(f"Eg:- \nGroup Discount Details \n\n {group}: 0.10 (10%)")
        print(f"Eg:- \nCustomer Details \n\n customer_id: 01 \n customer_name: John Doe \n customer_group: {group}")

        print(f"Final price of the Laptop \n = 350000*(1-0.15) \n = 350000*0.85 \n = 297500")
        print(f"\n {"="*100} \n")


    def loyalty_pricing_rules():
        pass

    def sub_menu():

        while True:
            print("Pricing Rule types")
            print(f"1. Tiered Pricing \n2. Grouped Pricing \n3. Loyalty Pricing \n99. Back")
            choice = int(input("Select Option (1, 2, 3): "))
            
            if choice == 1:
                PricingRule.tier_pricing_rules(Tier.SILVER)
                PricingRule.tier_pricing_rules(Tier.GOLD)
                PricingRule.tier_pricing_rules(Tier.PLATINUM)
            elif choice == 2:
                PricingRule.group_pricing_rules(Group.BULK)
                PricingRule.group_pricing_rules(Group.REGULAR)
                PricingRule.group_pricing_rules(Group.VIP)
            elif choice == 3:
                PricingRule.loyalty_pricing_rules()
            elif choice == 99:
                break

            else:
                print("Invalid option. Please Try Again")