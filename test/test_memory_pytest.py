"""
Unit Tests for Memory Data Storage using pytest
Tests all functionality of the Memory class including data storage, retrieval, and management.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.memory import Memory
from models.customer import Customer
from models.product import Product
from constants.tier import Tier
from constants.group import Group


class TestMemory:
    """Test suite for Memory class using pytest"""
    
    def setup_method(self):
        """Setup method to clear memory before each test"""
        Memory.clear_all()
    
    def test_memory_class_attributes_exist(self):
        """Test that Memory class has required class attributes"""
        assert hasattr(Memory, 'customers')
        assert hasattr(Memory, 'products')
        assert hasattr(Memory, 'orders')
        assert hasattr(Memory, 'results')
        
        assert isinstance(Memory.customers, list)
        assert isinstance(Memory.products, list)
        assert isinstance(Memory.orders, list)
        assert isinstance(Memory.results, list)
    
    def test_add_customer_with_loyalty_basic(self):
        """Test adding customer with basic loyalty pricing"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        loyalty_prices = [
            {"product_id": 1, "discount_rate": 0.15, "min_qty": 2}
        ]
        
        Memory.add_customer_with_loyalty(customer, loyalty_prices)
        
        assert len(Memory.customers) == 1
        assert Memory.customers[0][0] == customer
        assert Memory.customers[0][1] == loyalty_prices
    
    def test_add_customer_with_loyalty_no_loyalty(self):
        """Test adding customer without loyalty pricing"""
        customer = Customer(1, "John Doe", Tier.SILVER, [Group.REGULAR])
        
        Memory.add_customer_with_loyalty(customer)
        
        assert len(Memory.customers) == 1
        assert Memory.customers[0][0] == customer
        assert Memory.customers[0][1] == []
    
    def test_add_customer_with_loyalty_empty_list(self):
        """Test adding customer with empty loyalty list"""
        customer = Customer(1, "John Doe", Tier.PLATINUM, [Group.BULK])
        
        Memory.add_customer_with_loyalty(customer, [])
        
        assert len(Memory.customers) == 1
        assert Memory.customers[0][0] == customer
        assert Memory.customers[0][1] == []
    
    def test_add_multiple_customers(self):
        """Test adding multiple customers"""
        customer1 = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(2, "Jane Smith", Tier.SILVER, [Group.REGULAR])
        customer3 = Customer(3, "Bob Wilson", Tier.PLATINUM, [Group.BULK])
        
        loyalty1 = [{"product_id": 1, "discount_rate": 0.15, "min_qty": 2}]
        loyalty2 = [{"product_id": 2, "discount_rate": 0.10, "min_qty": 1}]
        
        Memory.add_customer_with_loyalty(customer1, loyalty1)
        Memory.add_customer_with_loyalty(customer2, loyalty2)
        Memory.add_customer_with_loyalty(customer3)  # No loyalty
        
        assert len(Memory.customers) == 3
        assert Memory.customers[0][0].customer_id == 1
        assert Memory.customers[1][0].customer_id == 2
        assert Memory.customers[2][0].customer_id == 3
        assert len(Memory.customers[2][1]) == 0  # No loyalty for customer3
    
    def test_add_product_with_pricing_basic(self):
        """Test adding product with basic pricing rules"""
        product = Product(1, "Laptop", 1000.0)
        tier_prices = [
            {"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}
        ]
        group_prices = [
            {"group": "VIP", "discount_rate": 0.15, "min_qty": 1}
        ]
        
        Memory.add_product_with_pricing(product, tier_prices, group_prices)
        
        assert len(Memory.products) == 1
        assert Memory.products[0][0] == product
        assert Memory.products[0][1] == tier_prices
        assert Memory.products[0][2] == group_prices
    
    def test_add_product_with_pricing_no_rules(self):
        """Test adding product without pricing rules"""
        product = Product(1, "Laptop", 1000.0)
        
        Memory.add_product_with_pricing(product)
        
        assert len(Memory.products) == 1
        assert Memory.products[0][0] == product
        assert Memory.products[0][1] == []
        assert Memory.products[0][2] == []
    
    def test_add_product_with_pricing_empty_lists(self):
        """Test adding product with empty pricing lists"""
        product = Product(1, "Laptop", 1000.0)
        
        Memory.add_product_with_pricing(product, [], [])
        
        assert len(Memory.products) == 1
        assert Memory.products[0][0] == product
        assert Memory.products[0][1] == []
        assert Memory.products[0][2] == []
    
    def test_add_multiple_products(self):
        """Test adding multiple products"""
        product1 = Product(1, "Laptop", 1000.0)
        product2 = Product(2, "Smartphone", 500.0)
        product3 = Product(3, "Tablet", 300.0)
        
        tier_prices1 = [{"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}]
        group_prices1 = [{"group": "VIP", "discount_rate": 0.15, "min_qty": 1}]
        
        tier_prices2 = [{"tier": "SILVER", "discount_rate": 0.05, "min_qty": 3}]
        
        Memory.add_product_with_pricing(product1, tier_prices1, group_prices1)
        Memory.add_product_with_pricing(product2, tier_prices2, [])
        Memory.add_product_with_pricing(product3)  # No pricing rules
        
        assert len(Memory.products) == 3
        assert Memory.products[0][0].product_id == 1
        assert Memory.products[1][0].product_id == 2
        assert Memory.products[2][0].product_id == 3
        assert len(Memory.products[2][1]) == 0  # No tier prices for product3
        assert len(Memory.products[2][2]) == 0  # No group prices for product3
    
    def test_add_order_basic(self):
        """Test adding basic order"""
        Memory.add_order(1, 2, 5)
        
        assert len(Memory.orders) == 1
        assert Memory.orders[0]['customer_id'] == 1
        assert Memory.orders[0]['product_id'] == 2
        assert Memory.orders[0]['quantity'] == 5
    
    def test_add_multiple_orders(self):
        """Test adding multiple orders"""
        Memory.add_order(1, 2, 5)
        Memory.add_order(3, 4, 10)
        Memory.add_order(1, 4, 2)  # Same customer, different product
        
        assert len(Memory.orders) == 3
        assert Memory.orders[0]['customer_id'] == 1
        assert Memory.orders[1]['customer_id'] == 3
        assert Memory.orders[2]['customer_id'] == 1
        assert Memory.orders[2]['product_id'] == 4
    
    def test_add_order_with_zero_values(self):
        """Test adding order with zero values"""
        Memory.add_order(0, 0, 0)
        
        assert len(Memory.orders) == 1
        assert Memory.orders[0]['customer_id'] == 0
        assert Memory.orders[0]['product_id'] == 0
        assert Memory.orders[0]['quantity'] == 0
    
    def test_add_order_with_negative_values(self):
        """Test adding order with negative values"""
        Memory.add_order(-1, -2, -5)
        
        assert len(Memory.orders) == 1
        assert Memory.orders[0]['customer_id'] == -1
        assert Memory.orders[0]['product_id'] == -2
        assert Memory.orders[0]['quantity'] == -5
    
    def test_add_result_basic(self):
        """Test adding basic result"""
        Memory.add_result("1", 850, "TIER")
        
        assert len(Memory.results) == 1
        assert Memory.results[0]['product_id'] == "1"
        assert Memory.results[0]['price'] == 850
        assert Memory.results[0]['price_type'] == "TIER"
    
    def test_add_multiple_results(self):
        """Test adding multiple results"""
        Memory.add_result("1", 850, "TIER")
        Memory.add_result("2", 425, "GROUP")
        Memory.add_result("3", 300, "BASE")
        
        assert len(Memory.results) == 3
        assert Memory.results[0]['price_type'] == "TIER"
        assert Memory.results[1]['price_type'] == "GROUP"
        assert Memory.results[2]['price_type'] == "BASE"
    
    def test_get_customer_by_id_found(self):
        """Test getting customer by ID when customer exists"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        loyalty_prices = [{"product_id": 1, "discount_rate": 0.15, "min_qty": 2}]
        
        Memory.add_customer_with_loyalty(customer, loyalty_prices)
        
        result = Memory.get_customer_by_id(1)
        
        assert result is not None
        assert result[0] == customer
        assert result[1] == loyalty_prices
    
    def test_get_customer_by_id_not_found(self):
        """Test getting customer by ID when customer doesn't exist"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        Memory.add_customer_with_loyalty(customer)
        
        result = Memory.get_customer_by_id(2)  # Different ID
        
        assert result is None
    
    def test_get_customer_by_id_multiple_customers(self):
        """Test getting customer by ID with multiple customers"""
        customer1 = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(2, "Jane Smith", Tier.SILVER, [Group.REGULAR])
        customer3 = Customer(3, "Bob Wilson", Tier.PLATINUM, [Group.BULK])
        
        Memory.add_customer_with_loyalty(customer1)
        Memory.add_customer_with_loyalty(customer2)
        Memory.add_customer_with_loyalty(customer3)
        
        result2 = Memory.get_customer_by_id(2)
        
        assert result2 is not None
        assert result2[0] == customer2
        assert result2[0].name == "Jane Smith"
    
    def test_get_product_by_id_found(self):
        """Test getting product by ID when product exists"""
        product = Product(1, "Laptop", 1000.0)
        tier_prices = [{"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}]
        group_prices = [{"group": "VIP", "discount_rate": 0.15, "min_qty": 1}]
        
        Memory.add_product_with_pricing(product, tier_prices, group_prices)
        
        result = Memory.get_product_by_id(1)
        
        assert result is not None
        assert result[0] == product
        assert result[1] == tier_prices
        assert result[2] == group_prices
    
    def test_get_product_by_id_not_found(self):
        """Test getting product by ID when product doesn't exist"""
        product = Product(1, "Laptop", 1000.0)
        Memory.add_product_with_pricing(product)
        
        result = Memory.get_product_by_id(2)  # Different ID
        
        assert result is None
    
    def test_get_product_by_id_multiple_products(self):
        """Test getting product by ID with multiple products"""
        product1 = Product(1, "Laptop", 1000.0)
        product2 = Product(2, "Smartphone", 500.0)
        product3 = Product(3, "Tablet", 300.0)
        
        Memory.add_product_with_pricing(product1)
        Memory.add_product_with_pricing(product2)
        Memory.add_product_with_pricing(product3)
        
        result2 = Memory.get_product_by_id(2)
        
        assert result2 is not None
        assert result2[0] == product2
        assert result2[0].name == "Smartphone"
    
    def test_get_all_customers_empty(self):
        """Test getting all customers when no customers exist"""
        result = Memory.get_all_customers()
        
        assert result == []
    
    def test_get_all_customers_single(self):
        """Test getting all customers with single customer"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        loyalty_prices = [{"product_id": 1, "discount_rate": 0.15, "min_qty": 2}]
        
        Memory.add_customer_with_loyalty(customer, loyalty_prices)
        
        result = Memory.get_all_customers()
        
        assert len(result) == 1
        assert result[0]['customer_id'] == 1
        assert result[0]['name'] == "John Doe"
        assert result[0]['tier'] == "GOLD"
        assert result[0]['groups'] == ["VIP"]
        assert result[0]['loyalty_products'] == loyalty_prices
    
    def test_get_all_customers_multiple(self):
        """Test getting all customers with multiple customers"""
        customer1 = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(2, "Jane Smith", Tier.SILVER, [Group.REGULAR, Group.BULK])
        
        loyalty1 = [{"product_id": 1, "discount_rate": 0.15, "min_qty": 2}]
        loyalty2 = []
        
        Memory.add_customer_with_loyalty(customer1, loyalty1)
        Memory.add_customer_with_loyalty(customer2, loyalty2)
        
        result = Memory.get_all_customers()
        
        assert len(result) == 2
        assert result[0]['customer_id'] == 1
        assert result[0]['groups'] == ["VIP"]
        assert result[1]['customer_id'] == 2
        assert result[1]['groups'] == ["REGULAR", "BULK"]
        assert result[1]['loyalty_products'] == []
    
    def test_get_all_products_empty(self):
        """Test getting all products when no products exist"""
        result = Memory.get_all_products()
        
        assert result == []
    
    def test_get_all_products_single(self):
        """Test getting all products with single product"""
        product = Product(1, "Laptop", 1000.0)
        tier_prices = [{"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}]
        group_prices = [{"group": "VIP", "discount_rate": 0.15, "min_qty": 1}]
        
        Memory.add_product_with_pricing(product, tier_prices, group_prices)
        
        result = Memory.get_all_products()
        
        assert len(result) == 1
        assert result[0]['product_id'] == 1
        assert result[0]['name'] == "Laptop"
        assert result[0]['base_price'] == 1000.0
        assert result[0]['tier_prices'] == tier_prices
        assert result[0]['group_prices'] == group_prices
    
    def test_get_all_products_multiple(self):
        """Test getting all products with multiple products"""
        product1 = Product(1, "Laptop", 1000.0)
        product2 = Product(2, "Smartphone", 500.0)
        
        tier_prices1 = [{"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}]
        group_prices1 = [{"group": "VIP", "discount_rate": 0.15, "min_qty": 1}]
        tier_prices2 = []
        group_prices2 = [{"group": "BULK", "discount_rate": 0.05, "min_qty": 5}]
        
        Memory.add_product_with_pricing(product1, tier_prices1, group_prices1)
        Memory.add_product_with_pricing(product2, tier_prices2, group_prices2)
        
        result = Memory.get_all_products()
        
        assert len(result) == 2
        assert result[0]['product_id'] == 1
        assert result[0]['base_price'] == 1000.0
        assert result[1]['product_id'] == 2
        assert result[1]['base_price'] == 500.0
        assert result[1]['tier_prices'] == []
    
    def test_clear_all(self):
        """Test clearing all data from memory"""
        # Add some data
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        product = Product(1, "Laptop", 1000.0)
        
        Memory.add_customer_with_loyalty(customer)
        Memory.add_product_with_pricing(product)
        Memory.add_order(1, 1, 5)
        Memory.add_result("1", 850, "TIER")
        
        # Verify data exists
        assert len(Memory.customers) == 1
        assert len(Memory.products) == 1
        assert len(Memory.orders) == 1
        assert len(Memory.results) == 1
        
        # Clear all
        Memory.clear_all()
        
        # Verify all data is cleared
        assert len(Memory.customers) == 0
        assert len(Memory.products) == 0
        assert len(Memory.orders) == 0
        assert len(Memory.results) == 0


class TestMemoryViewMethods:
    """Test the view methods of Memory class that print data"""
    
    def setup_method(self):
        """Setup method to clear memory before each test"""
        Memory.clear_all()
    
    def test_view_customers_empty(self, capsys):
        """Test view_customers with no customers"""
        Memory.view_customers()
        
        captured = capsys.readouterr()
        assert "No customers found." in captured.out
    
    def test_view_customers_single(self, capsys):
        """Test view_customers with single customer"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        loyalty_prices = [
            {"product_id": 1, "discount_rate": 0.15, "min_qty": 2},
            {"product_id": 2, "discount_rate": 0.10, "min_qty": 1}
        ]
        
        Memory.add_customer_with_loyalty(customer, loyalty_prices)
        Memory.view_customers()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Customer ID: 1" in output
        assert "Name: John Doe" in output
        assert "Tier: GOLD" in output
        assert "Groups: ['VIP']" in output
        assert "Loyalty Prices: 2 rules" in output
        assert "Product 1: 15.0% off, min qty 2" in output
        assert "Product 2: 10.0% off, min qty 1" in output
    
    def test_view_customers_multiple(self, capsys):
        """Test view_customers with multiple customers"""
        customer1 = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(2, "Jane Smith", Tier.SILVER, [Group.REGULAR])
        
        loyalty1 = [{"product_id": 1, "discount_rate": 0.15, "min_qty": 2}]
        loyalty2 = []
        
        Memory.add_customer_with_loyalty(customer1, loyalty1)
        Memory.add_customer_with_loyalty(customer2, loyalty2)
        
        Memory.view_customers()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Customer ID: 1" in output
        assert "Name: John Doe" in output
        assert "2. Customer ID: 2" in output
        assert "Name: Jane Smith" in output
        assert "Tier: SILVER" in output
        assert "Groups: ['REGULAR']" in output
        assert "Loyalty Prices: 0 rules" in output
    
    def test_view_products_empty(self, capsys):
        """Test view_products with no products"""
        Memory.view_products()
        
        captured = capsys.readouterr()
        assert "No products found." in captured.out
    
    def test_view_products_single(self, capsys):
        """Test view_products with single product"""
        product = Product(1, "Laptop", 1000.0)
        tier_prices = [
            {"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2},
            {"tier": "SILVER", "discount_rate": 0.05, "min_qty": 3}
        ]
        group_prices = [
            {"group": "VIP", "discount_rate": 0.15, "min_qty": 1}
        ]
        
        Memory.add_product_with_pricing(product, tier_prices, group_prices)
        Memory.view_products()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Product ID: 1" in output
        assert "Name: Laptop" in output
        assert "Base Price: 1000.0" in output
        assert "Tier Prices: 2 rules" in output
        assert "GOLD: 10.0% off, min qty 2" in output
        assert "SILVER: 5.0% off, min qty 3" in output
        assert "Group Prices: 1 rules" in output
        assert "VIP: 15.0% off, min qty 1" in output
    
    def test_view_products_multiple(self, capsys):
        """Test view_products with multiple products"""
        product1 = Product(1, "Laptop", 1000.0)
        product2 = Product(2, "Smartphone", 500.0)
        
        tier_prices1 = [{"tier": "GOLD", "discount_rate": 0.10, "min_qty": 2}]
        group_prices1 = []
        tier_prices2 = []
        group_prices2 = [{"group": "BULK", "discount_rate": 0.05, "min_qty": 5}]
        
        Memory.add_product_with_pricing(product1, tier_prices1, group_prices1)
        Memory.add_product_with_pricing(product2, tier_prices2, group_prices2)
        
        Memory.view_products()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Product ID: 1" in output
        assert "Name: Laptop" in output
        assert "2. Product ID: 2" in output
        assert "Name: Smartphone" in output
        assert "Base Price: 500.0" in output
        assert "Tier Prices: 0 rules" in output
        assert "Group Prices: 1 rules" in output
    
    def test_view_orders_empty(self, capsys):
        """Test view_orders with no orders"""
        Memory.view_orders()
        
        captured = capsys.readouterr()
        assert "No orders found." in captured.out
    
    def test_view_orders_single(self, capsys):
        """Test view_orders with single order"""
        Memory.add_order(1, 2, 5)
        Memory.view_orders()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Customer ID: 1, Product ID: 2, Quantity: 5" in output
    
    def test_view_orders_multiple(self, capsys):
        """Test view_orders with multiple orders"""
        Memory.add_order(1, 2, 5)
        Memory.add_order(3, 4, 10)
        Memory.add_order(1, 4, 2)
        
        Memory.view_orders()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Customer ID: 1, Product ID: 2, Quantity: 5" in output
        assert "2. Customer ID: 3, Product ID: 4, Quantity: 10" in output
        assert "3. Customer ID: 1, Product ID: 4, Quantity: 2" in output
    
    def test_view_results_empty(self, capsys):
        """Test view_results with no results"""
        Memory.view_results()
        
        captured = capsys.readouterr()
        assert "No results found." in captured.out
    
    def test_view_results_single(self, capsys):
        """Test view_results with single result"""
        Memory.add_result("1", 850, "TIER")
        Memory.view_results()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Product ID: 1, Price: 850, Type: TIER" in output
    
    def test_view_results_multiple(self, capsys):
        """Test view_results with multiple results"""
        Memory.add_result("1", 850, "TIER")
        Memory.add_result("2", 425, "GROUP")
        Memory.add_result("3", 300, "BASE")
        
        Memory.view_results()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "1. Product ID: 1, Price: 850, Type: TIER" in output
        assert "2. Product ID: 2, Price: 425, Type: GROUP" in output
        assert "3. Product ID: 3, Price: 300, Type: BASE" in output
    
    def test_clear_all_with_message(self, capsys):
        """Test clear_all method prints confirmation message"""
        Memory.clear_all()
        
        captured = capsys.readouterr()
        assert "All data cleared from memory." in captured.out


class TestMemoryEdgeCases:
    """Test edge cases and error conditions for Memory class"""
    
    def setup_method(self):
        """Setup method to clear memory before each test"""
        Memory.clear_all()
    
    def test_add_customer_with_none_loyalty(self):
        """Test adding customer with None loyalty (should default to empty list)"""
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        
        Memory.add_customer_with_loyalty(customer, None)
        
        assert len(Memory.customers) == 1
        assert Memory.customers[0][1] == []
    
    def test_add_product_with_none_pricing(self):
        """Test adding product with None pricing (should default to empty lists)"""
        product = Product(1, "Laptop", 1000.0)
        
        Memory.add_product_with_pricing(product, None, None)
        
        assert len(Memory.products) == 1
        assert Memory.products[0][1] == []
        assert Memory.products[0][2] == []
    
    def test_get_customer_by_id_with_zero_id(self):
        """Test getting customer with ID 0"""
        customer = Customer(0, "Test Customer", Tier.SILVER, [Group.REGULAR])
        Memory.add_customer_with_loyalty(customer)
        
        result = Memory.get_customer_by_id(0)
        
        assert result is not None
        assert result[0].customer_id == 0
    
    def test_get_product_by_id_with_zero_id(self):
        """Test getting product with ID 0"""
        product = Product(0, "Test Product", 100.0)
        Memory.add_product_with_pricing(product)
        
        result = Memory.get_product_by_id(0)
        
        assert result is not None
        assert result[0].product_id == 0
    
    def test_get_customer_by_id_with_negative_id(self):
        """Test getting customer with negative ID"""
        customer = Customer(-1, "Test Customer", Tier.SILVER, [Group.REGULAR])
        Memory.add_customer_with_loyalty(customer)
        
        result = Memory.get_customer_by_id(-1)
        
        assert result is not None
        assert result[0].customer_id == -1
    
    def test_memory_data_persistence_across_operations(self):
        """Test that memory data persists across different operations"""
        # Add initial data
        customer = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        product = Product(1, "Laptop", 1000.0)
        
        Memory.add_customer_with_loyalty(customer)
        Memory.add_product_with_pricing(product)
        Memory.add_order(1, 1, 5)
        Memory.add_result("1", 850, "TIER")
        
        # Perform operations
        result_customer = Memory.get_customer_by_id(1)
        result_product = Memory.get_product_by_id(1)
        all_customers = Memory.get_all_customers()
        all_products = Memory.get_all_products()
        
        # Verify data still exists
        assert result_customer is not None
        assert result_product is not None
        assert len(all_customers) == 1
        assert len(all_products) == 1
        assert len(Memory.orders) == 1
        assert len(Memory.results) == 1
    
    def test_memory_class_methods_are_class_methods(self):
        """Test that Memory methods are properly implemented as class methods"""
        # All methods should be callable on the class itself
        methods_to_test = [
            'add_customer_with_loyalty',
            'add_product_with_pricing',
            'add_order',
            'add_result',
            'get_customer_by_id',
            'get_product_by_id',
            'get_all_customers',
            'get_all_products',
            'view_customers',
            'view_products',
            'view_orders',
            'view_results',
            'clear_all'
        ]
        
        for method_name in methods_to_test:
            assert hasattr(Memory, method_name)
            assert callable(getattr(Memory, method_name))


class TestMemoryBusinessLogic:
    """Test business logic aspects of Memory class"""
    
    def setup_method(self):
        """Setup method to clear memory before each test"""
        Memory.clear_all()
    
    def test_realistic_e_commerce_scenario(self):
        """Test Memory with realistic e-commerce data"""
        # Add customers
        customer1 = Customer(1001, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(1002, "Jane Smith", Tier.SILVER, [Group.REGULAR])
        customer3 = Customer(1003, "Bob Wilson", Tier.PLATINUM, [Group.BULK])
        
        loyalty1 = [
            {"product_id": 1, "discount_rate": 0.20, "min_qty": 1},
            {"product_id": 2, "discount_rate": 0.15, "min_qty": 2}
        ]
        
        Memory.add_customer_with_loyalty(customer1, loyalty1)
        Memory.add_customer_with_loyalty(customer2, [])
        Memory.add_customer_with_loyalty(customer3, [])
        
        # Add products
        product1 = Product(1, "MacBook Pro", 2499.99)
        product2 = Product(2, "iPhone 15", 999.00)
        product3 = Product(3, "iPad Air", 599.99)
        
        tier_prices_mbp = [
            {"tier": "GOLD", "discount_rate": 0.10, "min_qty": 1},
            {"tier": "PLATINUM", "discount_rate": 0.15, "min_qty": 1}
        ]
        group_prices_mbp = [
            {"group": "VIP", "discount_rate": 0.12, "min_qty": 1},
            {"group": "BULK", "discount_rate": 0.08, "min_qty": 3}
        ]
        
        Memory.add_product_with_pricing(product1, tier_prices_mbp, group_prices_mbp)
        Memory.add_product_with_pricing(product2, [], [])
        Memory.add_product_with_pricing(product3, [], [])
        
        # Add orders
        Memory.add_order(1001, 1, 1)  # John buys MacBook
        Memory.add_order(1002, 2, 2)  # Jane buys 2 iPhones
        Memory.add_order(1003, 3, 5)  # Bob buys 5 iPads (bulk)
        Memory.add_order(1001, 2, 1)  # John also buys iPhone
        
        # Add results
        Memory.add_result("1", 2124.99, "LOYALTY")  # MacBook with loyalty discount
        Memory.add_result("2", 999.0, "BASE")      # iPhone at base price
        Memory.add_result("3", 2999.95, "BASE")    # iPads at base price
        Memory.add_result("2", 999.0, "BASE")      # John's iPhone
        
        # Verify the scenario
        assert len(Memory.customers) == 3
        assert len(Memory.products) == 3
        assert len(Memory.orders) == 4
        assert len(Memory.results) == 4
        
        # Test retrieval
        john = Memory.get_customer_by_id(1001)
        assert john is not None
        assert john[0].name == "John Doe"
        assert len(john[1]) == 2  # Has loyalty pricing
        
        macbook = Memory.get_product_by_id(1)
        assert macbook is not None
        assert macbook[0].name == "MacBook Pro"
        assert len(macbook[1]) == 2  # Has tier pricing
        assert len(macbook[2]) == 2  # Has group pricing
    
    def test_customer_order_relationship(self):
        """Test relationship between customers and their orders"""
        # Add customers
        customer1 = Customer(1, "John Doe", Tier.GOLD, [Group.VIP])
        customer2 = Customer(2, "Jane Smith", Tier.SILVER, [Group.REGULAR])
        
        Memory.add_customer_with_loyalty(customer1)
        Memory.add_customer_with_loyalty(customer2)
        
        # Add orders
        Memory.add_order(1, 1, 5)   # John's first order
        Memory.add_order(2, 2, 3)   # Jane's order
        Memory.add_order(1, 3, 2)   # John's second order
        Memory.add_order(1, 1, 1)   # John's third order (same product as first)
        
        # Analyze order patterns
        johns_orders = [order for order in Memory.orders if order['customer_id'] == 1]
        janes_orders = [order for order in Memory.orders if order['customer_id'] == 2]
        
        assert len(johns_orders) == 3
        assert len(janes_orders) == 1
        
        # John ordered product 1 twice
        product_1_orders = [order for order in johns_orders if order['product_id'] == 1]
        assert len(product_1_orders) == 2
        total_product_1_qty = sum(order['quantity'] for order in product_1_orders)
        assert total_product_1_qty == 6  # 5 + 1
    
    def test_product_pricing_complexity(self):
        """Test products with complex pricing structures"""
        product = Product(1, "Enterprise Software License", 10000.0)
        
        # Complex tier pricing
        tier_prices = [
            {"tier": "SILVER", "discount_rate": 0.05, "min_qty": 5},
            {"tier": "GOLD", "discount_rate": 0.10, "min_qty": 3},
            {"tier": "PLATINUM", "discount_rate": 0.20, "min_qty": 1}
        ]
        
        # Complex group pricing
        group_prices = [
            {"group": "REGULAR", "discount_rate": 0.02, "min_qty": 10},
            {"group": "BULK", "discount_rate": 0.15, "min_qty": 5},
            {"group": "VIP", "discount_rate": 0.25, "min_qty": 1}
        ]
        
        Memory.add_product_with_pricing(product, tier_prices, group_prices)
        
        result = Memory.get_product_by_id(1)
        
        assert result is not None
        assert len(result[1]) == 3  # 3 tier pricing rules
        assert len(result[2]) == 3  # 3 group pricing rules
        
        # Verify pricing rules are stored correctly
        tier_gold = next((tp for tp in result[1] if tp["tier"] == "GOLD"), None)
        assert tier_gold is not None
        assert tier_gold["discount_rate"] == 0.10
        assert tier_gold["min_qty"] == 3
        
        group_vip = next((gp for gp in result[2] if gp["group"] == "VIP"), None)
        assert group_vip is not None
        assert group_vip["discount_rate"] == 0.25
        assert group_vip["min_qty"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])