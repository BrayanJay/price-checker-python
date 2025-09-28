from group import Group
from tier import Tier

class Customer:

    """
    STRUCTURE
    {
    customer_id: 1,
    name: "Alice",
    tier: "Gold",
    groups: ["Regular", "VIP"],
    loyalty_customer: False
    }
    """
    customers = []

    def __init__(self, customer_id: int, name: str, tier: Tier, groups: list[Group], loyalty_customer: bool = False):
        self.customer_id = customer_id
        self.name = name
        self.tier = tier
        self.groups = groups
        self.loyalty_customer = loyalty_customer

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Tier: {self.tier.value}, Groups: {[group.value for group in self.groups]}, Loyalty Customer: {self.loyalty_customer}"

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_tier(self):
        return self.tier

    def get_groups(self):
        return self.groups

    def is_loyalty_customer(self):
        return self.loyalty_customer
    
    def set_loyalty_customer(self, loyalty_customer: bool):
        self.loyalty_customer = loyalty_customer

    @staticmethod
    def add_customer():
        print("Add New Customer")
        customer_id = int(input("Enter customer ID: "))
        name = input("Enter customer name: ")
        tier_input = input("Enter customer tier (Silver, Gold, Platinum): ").upper()
        tier = getattr(Tier, tier_input)
        
        num_groups = int(input("Enter number of groups: "))
        groups = []
        for i in range(num_groups):
            group_input = input(f"Enter group {i + 1} (Regular, Bulk, VIP): ").upper()
            groups.append(getattr(Group, group_input))
        
        loyalty_customer = input("Is this a loyalty customer? (yes/no): ").lower() == "yes"

        Customer.customers.append({
            "customer_id": customer_id,
            "name": name,
            "tier": tier.value,
            "groups": [group.value for group in groups],
            "loyalty_customer": loyalty_customer
        })

    @staticmethod
    def view_customers():
        if not Customer.customers:
            print("No customers available.")
        else:
            for customer in Customer.customers:
                print(customer)

    @staticmethod
    def get_customer(customer_id: int):
        for customer in Customer.customers:
            if customer['customer_id'] == customer_id:
                return customer
        return None

    @staticmethod
    def update_customer(customer_id: int):
        customer = Customer.get_customer(customer_id)
        if customer:
            print("Update Customer")
            new_name = input(f"Enter new name (current: {customer['name']}): ")
            if new_name:
                customer['name'] = new_name
            
            tier_input = input(f"Enter new tier (current: {customer['tier']}) (Silver, Gold, Platinum): ")
            if tier_input:
                customer['tier'] = getattr(Tier, tier_input.upper()).value
            
            new_groups = []
            for i, group in enumerate(customer['groups']):
                group_input = input(f"Enter new group {i + 1} (current: {group}) (Regular, Bulk, VIP): ")
                if group_input:
                    new_groups.append(getattr(Group, group_input.upper()).value)
                else:
                    new_groups.append(group)
            customer['groups'] = new_groups
            
            loyalty_input = input(f"Is this a loyalty customer? (current: {customer['loyalty_customer']}) (yes/no): ")
            if loyalty_input:
                customer['loyalty_customer'] = loyalty_input.lower() == "yes"
            
            print("Customer updated successfully.")
        else:
            print("Customer not found.")

    @staticmethod
    def delete_customer(customer_id: int):
        customer = Customer.get_customer(customer_id)
        if customer:
            Customer.customers.remove(customer)
            print("Customer deleted successfully.")
        else:
            print("Customer not found.")