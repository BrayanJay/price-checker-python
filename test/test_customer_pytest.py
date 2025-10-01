"""
Unit Tests for Customer Model using pytest
Tests all functionality of the Customer class including creation, validation, and static methods.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.customer import Customer
from constants.tier import Tier
from constants.group import Group


class TestCustomer:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):

        # Clear the customers list before each test
        Customer.customers = []
    
    def test_customer_initialization(self):

        customer = Customer(
            customer_id=1,
            name="John Doe",
            tier=Tier.GOLD,
            groups=[Group.REGULAR, Group.VIP],
            loyalty_customer=True
        )
        
        assert customer.customer_id == 1
        assert customer.name == "John Doe"
        assert customer.tier == Tier.GOLD
        assert customer.groups == [Group.REGULAR, Group.VIP]
        assert customer.loyalty_customer == True
    
    def test_customer_initialization_default_loyalty(self):

        customer = Customer(
            customer_id=2,
            name="Jane Smith",
            tier=Tier.SILVER,
            groups=[Group.BULK]
        )
        
        assert customer.customer_id == 2
        assert customer.name == "Jane Smith"
        assert customer.tier == Tier.SILVER
        assert customer.groups == [Group.BULK]
        assert customer.loyalty_customer == False  # Default value
    
    def test_customer_str_representation(self):

        customer = Customer(
            customer_id=3,
            name="Bob Johnson",
            tier=Tier.PLATINUM,
            groups=[Group.VIP, Group.BULK],
            loyalty_customer=True
        )
        
        expected_str = "Customer ID: 3, Name: Bob Johnson, Tier: PLATINUM, Groups: ['VIP', 'Bulk'], Loyalty Customer: True"
        assert str(customer) == expected_str
    
    def test_get_customer_id(self):

        customer = Customer(1, "Test", Tier.GOLD, [Group.REGULAR])
        assert customer.get_customer_id() == 1
    
    def test_get_name(self):

        customer = Customer(1, "Alice Wonder", Tier.GOLD, [Group.REGULAR])
        assert customer.get_name() == "Alice Wonder"
    
    def test_get_tier(self):

        customer = Customer(1, "Test", Tier.SILVER, [Group.REGULAR])
        assert customer.get_tier() == Tier.SILVER
    
    def test_get_groups(self):

        groups = [Group.VIP, Group.BULK]
        customer = Customer(1, "Test", Tier.GOLD, groups)
        assert customer.get_groups() == groups
    
    def test_is_loyalty_customer(self):

        customer = Customer(1, "Test", Tier.GOLD, [Group.REGULAR], True)
        assert customer.is_loyalty_customer() == True
        
        customer2 = Customer(2, "Test2", Tier.GOLD, [Group.REGULAR], False)
        assert customer2.is_loyalty_customer() == False
    
    def test_set_loyalty_customer(self):

        customer = Customer(1, "Test", Tier.GOLD, [Group.REGULAR], False)
        assert customer.is_loyalty_customer() == False
        
        customer.set_loyalty_customer(True)
        assert customer.is_loyalty_customer() == True
        
        customer.set_loyalty_customer(False)
        assert customer.is_loyalty_customer() == False
    
    @patch('builtins.input')
    def test_add_customer_success(self, mock_input):

        # Mock user inputs
        mock_input.side_effect = [
            '1',          # customer_id
            'Test User',  # name
            'silver',     # tier
            '2',          # num_groups
            'regular',    # group 1
            'vip',        # group 2
            'yes'         # loyalty_customer
        ]
        
        # Call the static method
        Customer.add_customer()
        
        # Verify customer was added
        assert len(Customer.customers) == 1
        customer_data = Customer.customers[0]
        
        assert customer_data['customer_id'] == 1
        assert customer_data['name'] == 'Test User'
        assert customer_data['tier'] == 'SILVER'
        assert customer_data['groups'] == ['Regular', 'VIP']
        assert customer_data['loyalty_customer'] == True
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_add_customer_invalid_tier(self, mock_print, mock_input):

        mock_input.side_effect = [
            '1',           # customer_id
            'Test User',   # name
            'invalid',     # invalid tier
        ]
        
        Customer.add_customer()
        
        # Verify no customer was added
        assert len(Customer.customers) == 0
        
        # Verify error message was printed
        mock_print.assert_any_call("Invalid tier 'invalid'. Available tiers: SILVER, GOLD, PLATINUM")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_add_customer_invalid_group(self, mock_print, mock_input):

        mock_input.side_effect = [
            '1',           # customer_id
            'Test User',   # name
            'gold',        # tier
            '1',           # num_groups
            'invalid',     # invalid group
        ]
        
        Customer.add_customer()
        
        # Verify no customer was added
        assert len(Customer.customers) == 0
        
        # Verify error message was printed
        mock_print.assert_any_call("Invalid group 'invalid'. Available groups: Regular, Bulk, VIP")
    
    def test_view_customers_empty(self, capsys):

        Customer.view_customers()
        captured = capsys.readouterr()
        assert "No customers available." in captured.out
    
    def test_view_customers_with_data(self, capsys):

        # Add sample customer data
        Customer.customers = [
            {
                'customer_id': 1,
                'name': 'John Doe',
                'tier': 'GOLD',
                'groups': ['Regular', 'VIP'],
                'loyalty_customer': True
            }
        ]
        
        Customer.view_customers()
        captured = capsys.readouterr()
        assert "{'customer_id': 1" in captured.out
    
    def test_get_customer_found(self):

        # Add sample customer data
        Customer.customers = [
            {
                'customer_id': 1,
                'name': 'John Doe',
                'tier': 'GOLD',
                'groups': ['Regular'],
                'loyalty_customer': False
            }
        ]
        
        result = Customer.get_customer(1)
        assert result is not None
        assert result['customer_id'] == 1
        assert result['name'] == 'John Doe'
    
    def test_get_customer_not_found(self):

        result = Customer.get_customer(999)
        assert result is None
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_update_customer_success(self, mock_print, mock_input):

        # Add sample customer data
        Customer.customers = [
            {
                'customer_id': 1,
                'name': 'Old Name',
                'tier': 'SILVER',
                'groups': ['Regular'],
                'loyalty_customer': False
            }
        ]
        
        mock_input.side_effect = [
            'New Name',    # new_name
            'gold',        # new tier
            'vip',         # new group 1
            'yes'          # loyalty_customer
        ]
        
        Customer.update_customer(1)
        
        # Verify customer was updated
        customer = Customer.customers[0]
        assert customer['name'] == 'New Name'
        assert customer['tier'] == 'GOLD'
        assert customer['groups'] == ['VIP']
        assert customer['loyalty_customer'] == True
        
        mock_print.assert_any_call("Customer updated successfully.")
    
    @patch('builtins.print')
    def test_update_customer_not_found(self, mock_print):

        Customer.update_customer(999)
        mock_print.assert_called_with("Customer not found.")
    
    def test_delete_customer_success(self, capsys):

        # Add sample customer data
        customer_data = {
            'customer_id': 1,
            'name': 'Test User',
            'tier': 'GOLD',
            'groups': ['Regular'],
            'loyalty_customer': False
        }
        Customer.customers = [customer_data]
        
        Customer.delete_customer(1)
        
        # Verify customer was deleted
        assert len(Customer.customers) == 0
        
        captured = capsys.readouterr()
        assert "Customer deleted successfully." in captured.out
    
    def test_delete_customer_not_found(self, capsys):

        Customer.delete_customer(999)
        
        captured = capsys.readouterr()
        assert "Customer not found." in captured.out
    
    def test_customer_with_multiple_groups(self):

        groups = [Group.REGULAR, Group.BULK, Group.VIP]
        customer = Customer(1, "Multi Group User", Tier.PLATINUM, groups)
        
        assert len(customer.get_groups()) == 3
        assert Group.REGULAR in customer.get_groups()
        assert Group.BULK in customer.get_groups()
        assert Group.VIP in customer.get_groups()
    
    def test_customer_with_single_group(self):

        groups = [Group.VIP]
        customer = Customer(1, "VIP User", Tier.GOLD, groups)
        
        assert len(customer.get_groups()) == 1
        assert customer.get_groups()[0] == Group.VIP
    
    def test_customer_equality_by_id(self):

        customer1 = Customer(1, "User 1", Tier.GOLD, [Group.REGULAR])
        customer2 = Customer(1, "Different Name", Tier.SILVER, [Group.VIP])
        
        # Same ID should be considered for uniqueness
        assert customer1.get_customer_id() == customer2.get_customer_id()
    
    def test_loyalty_customer_toggle(self):

        customer = Customer(1, "Toggle User", Tier.GOLD, [Group.REGULAR])
        
        # Default should be False
        assert not customer.is_loyalty_customer()
        
        # Toggle to True
        customer.set_loyalty_customer(True)
        assert customer.is_loyalty_customer()
        
        # Toggle back to False
        customer.set_loyalty_customer(False)
        assert not customer.is_loyalty_customer()


class TestCustomerClassAttributes:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):

        Customer.customers = []
    
    def test_customers_list_is_shared(self):

        # Add data via static method
        Customer.customers.append({"customer_id": 1, "name": "Test"})
        
        # Should be accessible from class
        assert len(Customer.customers) == 1
        
        # Clear via class
        Customer.customers.clear()
        assert len(Customer.customers) == 0
    
    def test_customers_list_persistence(self):

        # Add multiple customers
        Customer.customers.extend([
            {"customer_id": 1, "name": "User 1"},
            {"customer_id": 2, "name": "User 2"},
            {"customer_id": 3, "name": "User 3"}
        ])
        
        assert len(Customer.customers) == 3
        
        # Delete one customer
        Customer.delete_customer(2)
        assert len(Customer.customers) == 2
        
        # Verify the right customer was deleted
        customer_ids = [c["customer_id"] for c in Customer.customers]
        assert 2 not in customer_ids
        assert 1 in customer_ids
        assert 3 in customer_ids


if __name__ == "__main__":
    pytest.main([__file__])