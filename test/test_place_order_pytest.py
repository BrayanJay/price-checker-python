"""
Unit Tests for PlaceOrder Model using pytest
Tests all functionality of the PlaceOrder class including order creation, storage, and viewing.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.place_order import PlaceOrder


class TestPlaceOrder:
    """Test suite for PlaceOrder class using pytest"""
    
    def setup_method(self):
        """Setup method to clear orders before each test"""
        PlaceOrder.placed_orders.clear()
    
    def test_place_order_initialization(self):
        """Test PlaceOrder object initialization"""
        order = PlaceOrder(
            product_id=1,
            quantity=5,
            customer_id=100
        )
        
        assert order.product_id == 1
        assert order.quantity == 5
        assert order.customer_id == 100
    
    def test_place_order_initialization_zero_values(self):
        """Test PlaceOrder initialization with zero values"""
        order = PlaceOrder(
            product_id=0,
            quantity=0,
            customer_id=0
        )
        
        assert order.product_id == 0
        assert order.quantity == 0
        assert order.customer_id == 0
    
    def test_place_order_initialization_negative_values(self):
        """Test PlaceOrder initialization with negative values"""
        order = PlaceOrder(
            product_id=-1,
            quantity=-5,
            customer_id=-100
        )
        
        assert order.product_id == -1
        assert order.quantity == -5
        assert order.customer_id == -100
    
    def test_place_order_initialization_large_values(self):
        """Test PlaceOrder initialization with large values"""
        order = PlaceOrder(
            product_id=999999,
            quantity=10000,
            customer_id=888888
        )
        
        assert order.product_id == 999999
        assert order.quantity == 10000
        assert order.customer_id == 888888
    
    def test_place_order_attributes_are_accessible(self):
        """Test that order attributes are directly accessible"""
        order = PlaceOrder(1, 2, 3)
        
        # Test direct attribute access
        assert hasattr(order, 'product_id')
        assert hasattr(order, 'quantity')
        assert hasattr(order, 'customer_id')
        
        # Test attribute modification
        order.product_id = 10
        order.quantity = 20
        order.customer_id = 30
        
        assert order.product_id == 10
        assert order.quantity == 20
        assert order.customer_id == 30
    
    def test_place_order_class_attribute_exists(self):
        """Test that placed_orders class attribute exists and is a list"""
        assert hasattr(PlaceOrder, 'placed_orders')
        assert isinstance(PlaceOrder.placed_orders, list)
    
    def test_append_order_static_method(self):
        """Test append_order static method"""
        order = PlaceOrder(1, 5, 100)
        
        # Initially empty
        assert len(PlaceOrder.placed_orders) == 0
        
        # Append order
        PlaceOrder.append_order(order)
        
        # Check if order was added
        assert len(PlaceOrder.placed_orders) == 1
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        assert PlaceOrder.placed_orders[0]['quantity'] == 5
        assert PlaceOrder.placed_orders[0]['customer_id'] == 100
    
    def test_append_multiple_orders(self):
        """Test appending multiple orders"""
        order1 = PlaceOrder(1, 5, 100)
        order2 = PlaceOrder(2, 10, 200)
        order3 = PlaceOrder(3, 15, 300)
        
        PlaceOrder.append_order(order1)
        PlaceOrder.append_order(order2)
        PlaceOrder.append_order(order3)
        
        assert len(PlaceOrder.placed_orders) == 3
        
        # Check first order
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        assert PlaceOrder.placed_orders[0]['quantity'] == 5
        assert PlaceOrder.placed_orders[0]['customer_id'] == 100
        
        # Check second order
        assert PlaceOrder.placed_orders[1]['product_id'] == 2
        assert PlaceOrder.placed_orders[1]['quantity'] == 10
        assert PlaceOrder.placed_orders[1]['customer_id'] == 200
        
        # Check third order
        assert PlaceOrder.placed_orders[2]['product_id'] == 3
        assert PlaceOrder.placed_orders[2]['quantity'] == 15
        assert PlaceOrder.placed_orders[2]['customer_id'] == 300
    
    def test_append_order_with_same_data(self):
        """Test appending orders with same data (should be allowed)"""
        order1 = PlaceOrder(1, 5, 100)
        order2 = PlaceOrder(1, 5, 100)  # Same data
        
        PlaceOrder.append_order(order1)
        PlaceOrder.append_order(order2)
        
        assert len(PlaceOrder.placed_orders) == 2
        
        # Both orders should be in the list
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        assert PlaceOrder.placed_orders[1]['product_id'] == 1
    
    def test_view_orders_with_empty_list(self, capsys):
        """Test view_orders method with empty orders list"""
        # Ensure list is empty
        PlaceOrder.placed_orders.clear()
        
        PlaceOrder.view_orders()
        
        captured = capsys.readouterr()
        assert "No orders placed." in captured.out
    
    def test_view_orders_with_single_order(self, capsys):
        """Test view_orders method with single order"""
        order = PlaceOrder(1, 5, 100)
        PlaceOrder.append_order(order)
        
        PlaceOrder.view_orders()
        
        captured = capsys.readouterr()
        assert "Order - Product ID: 1, Quantity: 5, Customer ID: 100" in captured.out
    
    def test_view_orders_with_multiple_orders(self, capsys):
        """Test view_orders method with multiple orders"""
        order1 = PlaceOrder(1, 5, 100)
        order2 = PlaceOrder(2, 10, 200)
        order3 = PlaceOrder(3, 15, 300)
        
        PlaceOrder.append_order(order1)
        PlaceOrder.append_order(order2)
        PlaceOrder.append_order(order3)
        
        PlaceOrder.view_orders()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Order - Product ID: 1, Quantity: 5, Customer ID: 100" in output
        assert "Order - Product ID: 2, Quantity: 10, Customer ID: 200" in output
        assert "Order - Product ID: 3, Quantity: 15, Customer ID: 300" in output
    
    @patch('builtins.input', side_effect=['1', '5', '100'])
    def test_add_order_static_method(self, mock_input, capsys):
        """Test add_order static method with mocked input"""
        PlaceOrder.add_order()
        
        # Check if order was added to placed_orders
        assert len(PlaceOrder.placed_orders) == 1
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        assert PlaceOrder.placed_orders[0]['quantity'] == 5
        assert PlaceOrder.placed_orders[0]['customer_id'] == 100
        
        # Check if success message was printed
        captured = capsys.readouterr()
        assert "Order Placed Successfully!" in captured.out
    
    @patch('builtins.input', side_effect=['999', '25', '777'])
    def test_add_order_with_large_values(self, mock_input):
        """Test add_order static method with large values"""
        PlaceOrder.add_order()
        
        assert len(PlaceOrder.placed_orders) == 1
        assert PlaceOrder.placed_orders[0]['product_id'] == 999
        assert PlaceOrder.placed_orders[0]['quantity'] == 25
        assert PlaceOrder.placed_orders[0]['customer_id'] == 777
    
    @patch('builtins.input', side_effect=['0', '0', '0'])
    def test_add_order_with_zero_values(self, mock_input):
        """Test add_order static method with zero values"""
        PlaceOrder.add_order()
        
        assert len(PlaceOrder.placed_orders) == 1
        assert PlaceOrder.placed_orders[0]['product_id'] == 0
        assert PlaceOrder.placed_orders[0]['quantity'] == 0
        assert PlaceOrder.placed_orders[0]['customer_id'] == 0
    
    def test_order_data_structure(self):
        """Test the structure of order data stored in placed_orders"""
        order = PlaceOrder(123, 456, 789)
        PlaceOrder.append_order(order)
        
        stored_order = PlaceOrder.placed_orders[0]
        
        # Check that stored order is a dictionary
        assert isinstance(stored_order, dict)
        
        # Check required keys exist
        assert 'product_id' in stored_order
        assert 'quantity' in stored_order
        assert 'customer_id' in stored_order
        
        # Check values match
        assert stored_order['product_id'] == 123
        assert stored_order['quantity'] == 456
        assert stored_order['customer_id'] == 789
    
    def test_order_independence(self):
        """Test that modifying original order doesn't affect stored order"""
        order = PlaceOrder(1, 5, 100)
        PlaceOrder.append_order(order)
        
        # Modify original order
        order.product_id = 999
        order.quantity = 888
        order.customer_id = 777
        
        # Check that stored order is unchanged
        stored_order = PlaceOrder.placed_orders[0]
        assert stored_order['product_id'] == 1
        assert stored_order['quantity'] == 5
        assert stored_order['customer_id'] == 100
    
    def test_multiple_order_instances_with_same_class_list(self):
        """Test that multiple order instances share the same class-level list"""
        order1 = PlaceOrder(1, 5, 100)
        order2 = PlaceOrder(2, 10, 200)
        
        # Both should reference the same class-level list
        assert order1.placed_orders is order2.placed_orders
        assert order1.placed_orders is PlaceOrder.placed_orders
    
    def test_order_string_representation(self):
        """Test string representation of PlaceOrder (if __str__ method exists)"""
        order = PlaceOrder(1, 5, 100)
        
        # Since PlaceOrder class doesn't define __str__, it will use default
        str_repr = str(order)
        assert "PlaceOrder" in str_repr  # Should contain class name
        assert "object at" in str_repr  # Default object representation


class TestPlaceOrderEdgeCases:
    """Test edge cases and error conditions for PlaceOrder class"""
    
    def setup_method(self):
        """Setup method to clear orders before each test"""
        PlaceOrder.placed_orders.clear()
    
    def test_place_order_with_none_values(self):
        """Test PlaceOrder creation with None values (should raise errors)"""
        with pytest.raises(TypeError):
            PlaceOrder(None, 5, 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, None, 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, 5, None)
    
    def test_place_order_with_string_values(self):
        """Test PlaceOrder creation with string values (should raise errors)"""
        with pytest.raises(TypeError):
            PlaceOrder("1", 5, 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, "5", 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, 5, "100")
    
    def test_place_order_with_float_values(self):
        """Test PlaceOrder creation with float values (should raise errors)"""
        with pytest.raises(TypeError):
            PlaceOrder(1.5, 5, 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, 5.5, 100)
        
        with pytest.raises(TypeError):
            PlaceOrder(1, 5, 100.5)
    
    @patch('builtins.input', side_effect=['abc', '5', '100'])
    def test_add_order_with_invalid_input(self, mock_input):
        """Test add_order static method with invalid input"""
        with pytest.raises(ValueError):
            PlaceOrder.add_order()
    
    @patch('builtins.input', side_effect=['1', 'xyz', '100'])
    def test_add_order_with_invalid_quantity_input(self, mock_input):
        """Test add_order static method with invalid quantity input"""
        with pytest.raises(ValueError):
            PlaceOrder.add_order()
    
    @patch('builtins.input', side_effect=['1', '5', 'invalid'])
    def test_add_order_with_invalid_customer_input(self, mock_input):
        """Test add_order static method with invalid customer input"""
        with pytest.raises(ValueError):
            PlaceOrder.add_order()
    
    def test_direct_manipulation_of_placed_orders(self):
        """Test direct manipulation of the placed_orders class attribute"""
        # Direct manipulation should be possible but not recommended
        initial_length = len(PlaceOrder.placed_orders)
        
        # Add directly to the list
        PlaceOrder.placed_orders.append({
            "product_id": 999,
            "quantity": 888,
            "customer_id": 777
        })
        
        assert len(PlaceOrder.placed_orders) == initial_length + 1
        assert PlaceOrder.placed_orders[-1]['product_id'] == 999
    
    def test_order_data_immutability(self):
        """Test that stored order data can be modified (not immutable)"""
        order = PlaceOrder(1, 5, 100)
        PlaceOrder.append_order(order)
        
        # Modify stored order data
        PlaceOrder.placed_orders[0]['product_id'] = 999
        PlaceOrder.placed_orders[0]['quantity'] = 888
        PlaceOrder.placed_orders[0]['customer_id'] = 777
        
        # Check modifications
        assert PlaceOrder.placed_orders[0]['product_id'] == 999
        assert PlaceOrder.placed_orders[0]['quantity'] == 888
        assert PlaceOrder.placed_orders[0]['customer_id'] == 777


class TestPlaceOrderDataTypes:
    """Test various data types with PlaceOrder class"""
    
    def setup_method(self):
        """Setup method to clear orders before each test"""
        PlaceOrder.placed_orders.clear()
    
    def test_place_order_with_different_int_types(self):
        """Test PlaceOrder with different integer types"""
        # Regular int
        order1 = PlaceOrder(1, 5, 100)
        assert order1.product_id == 1
        assert order1.quantity == 5
        assert order1.customer_id == 100
        
        # Large int
        large_values = (999999999, 888888888, 777777777)
        order2 = PlaceOrder(*large_values)
        assert order2.product_id == 999999999
        assert order2.quantity == 888888888
        assert order2.customer_id == 777777777
        
        # Zero
        order3 = PlaceOrder(0, 0, 0)
        assert order3.product_id == 0
        assert order3.quantity == 0
        assert order3.customer_id == 0
        
        # Negative
        order4 = PlaceOrder(-1, -5, -100)
        assert order4.product_id == -1
        assert order4.quantity == -5
        assert order4.customer_id == -100
    
    def test_placed_orders_persistence(self):
        """Test that placed_orders list persists across instances"""
        order1 = PlaceOrder(1, 5, 100)
        PlaceOrder.append_order(order1)
        
        # Create new instance
        order2 = PlaceOrder(2, 10, 200)
        
        # First order should still be in the list
        assert len(PlaceOrder.placed_orders) == 1
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        
        # Add second order
        PlaceOrder.append_order(order2)
        
        # Both orders should be in the list
        assert len(PlaceOrder.placed_orders) == 2


class TestPlaceOrderBusinessLogic:
    """Test business logic aspects of PlaceOrder class"""
    
    def setup_method(self):
        """Setup method to clear orders before each test"""
        PlaceOrder.placed_orders.clear()
    
    def test_realistic_e_commerce_orders(self):
        """Test order creation with realistic e-commerce data"""
        orders_data = [
            (1, 2, 1001),      # Product 1, Quantity 2, Customer 1001
            (2, 1, 1002),      # Product 2, Quantity 1, Customer 1002
            (3, 5, 1001),      # Product 3, Quantity 5, Customer 1001 (repeat customer)
            (1, 10, 1003),     # Product 1, Quantity 10, Customer 1003 (bulk order)
            (4, 1, 1004)       # Product 4, Quantity 1, Customer 1004
        ]
        
        for product_id, quantity, customer_id in orders_data:
            order = PlaceOrder(product_id, quantity, customer_id)
            PlaceOrder.append_order(order)
        
        assert len(PlaceOrder.placed_orders) == 5
        
        # Check specific orders
        assert PlaceOrder.placed_orders[0]['product_id'] == 1
        assert PlaceOrder.placed_orders[0]['quantity'] == 2
        assert PlaceOrder.placed_orders[0]['customer_id'] == 1001
        
        assert PlaceOrder.placed_orders[3]['quantity'] == 10  # Bulk order
    
    def test_order_analytics_operations(self):
        """Test operations that might be performed for order analytics"""
        # Create sample orders
        orders_data = [
            (1, 2, 1001),
            (2, 1, 1002),
            (1, 5, 1001),   # Same customer, same product
            (3, 10, 1003),
            (2, 3, 1004)
        ]
        
        for product_id, quantity, customer_id in orders_data:
            order = PlaceOrder(product_id, quantity, customer_id)
            PlaceOrder.append_order(order)
        
        # Test finding orders by customer
        customer_1001_orders = [
            order for order in PlaceOrder.placed_orders 
            if order['customer_id'] == 1001
        ]
        assert len(customer_1001_orders) == 2
        
        # Test finding orders by product
        product_1_orders = [
            order for order in PlaceOrder.placed_orders 
            if order['product_id'] == 1
        ]
        assert len(product_1_orders) == 2
        
        # Test calculating total quantity for a product
        total_product_1_qty = sum(
            order['quantity'] for order in PlaceOrder.placed_orders 
            if order['product_id'] == 1
        )
        assert total_product_1_qty == 7  # 2 + 5
        
        # Test finding bulk orders (quantity > 5)
        bulk_orders = [
            order for order in PlaceOrder.placed_orders 
            if order['quantity'] > 5
        ]
        assert len(bulk_orders) == 1
        assert bulk_orders[0]['quantity'] == 10
    
    def test_order_sorting_and_filtering(self):
        """Test sorting and filtering operations on orders"""
        # Create orders with different quantities
        orders_data = [
            (1, 10, 1001),
            (2, 1, 1002),
            (3, 5, 1003),
            (4, 20, 1004),
            (5, 3, 1005)
        ]
        
        for product_id, quantity, customer_id in orders_data:
            order = PlaceOrder(product_id, quantity, customer_id)
            PlaceOrder.append_order(order)
        
        # Test sorting by quantity
        sorted_by_quantity = sorted(
            PlaceOrder.placed_orders, 
            key=lambda x: x['quantity']
        )
        assert sorted_by_quantity[0]['quantity'] == 1
        assert sorted_by_quantity[-1]['quantity'] == 20
        
        # Test sorting by customer_id
        sorted_by_customer = sorted(
            PlaceOrder.placed_orders, 
            key=lambda x: x['customer_id']
        )
        assert sorted_by_customer[0]['customer_id'] == 1001
        assert sorted_by_customer[-1]['customer_id'] == 1005
        
        # Test filtering by quantity range
        medium_orders = [
            order for order in PlaceOrder.placed_orders 
            if 3 <= order['quantity'] <= 10
        ]
        assert len(medium_orders) == 3  # quantities 10, 5, 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])