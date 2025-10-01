"""
Unit Tests for Product Model using pytest
Tests all functionality of the Product class including creation and validation.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product import Product


class TestProduct:
    """Test suite for Product class using pytest"""
    
    def test_product_initialization(self):
        """Test Product object initialization"""
        product = Product(
            product_id=1,
            name="Laptop",
            base_price=1200.50
        )
        
        assert product.product_id == 1
        assert product.name == "Laptop"
        assert product.base_price == 1200.50
    
    def test_product_initialization_integer_price(self):
        """Test Product initialization with integer price"""
        product = Product(
            product_id=2,
            name="Smartphone",
            base_price=800
        )
        
        assert product.product_id == 2
        assert product.name == "Smartphone"
        assert product.base_price == 800.0  # Should be converted to float
    
    def test_product_initialization_zero_price(self):
        """Test Product initialization with zero price"""
        product = Product(
            product_id=3,
            name="Free Sample",
            base_price=0.0
        )
        
        assert product.product_id == 3
        assert product.name == "Free Sample"
        assert product.base_price == 0.0
    
    def test_product_initialization_negative_id(self):
        """Test Product initialization with negative ID"""
        product = Product(
            product_id=-1,
            name="Test Product",
            base_price=100.0
        )
        
        assert product.product_id == -1
        assert product.name == "Test Product"
        assert product.base_price == 100.0
    
    def test_product_with_empty_name(self):
        """Test Product with empty name"""
        product = Product(
            product_id=1,
            name="",
            base_price=100.0
        )
        
        assert product.product_id == 1
        assert product.name == ""
        assert product.base_price == 100.0
    
    def test_product_with_long_name(self):
        """Test Product with very long name"""
        long_name = "A" * 1000  # Very long product name
        product = Product(
            product_id=1,
            name=long_name,
            base_price=100.0
        )
        
        assert product.product_id == 1
        assert product.name == long_name
        assert len(product.name) == 1000
        assert product.base_price == 100.0
    
    def test_product_with_special_characters_in_name(self):
        """Test Product with special characters in name"""
        special_name = "Product @#$%^&*()_+-={}[]|\\:;\"'<>,.?/"
        product = Product(
            product_id=1,
            name=special_name,
            base_price=100.0
        )
        
        assert product.product_id == 1
        assert product.name == special_name
        assert product.base_price == 100.0
    
    def test_product_with_unicode_name(self):
        """Test Product with Unicode characters in name"""
        unicode_name = "Продукт 产品 製品 produit"
        product = Product(
            product_id=1,
            name=unicode_name,
            base_price=100.0
        )
        
        assert product.product_id == 1
        assert product.name == unicode_name
        assert product.base_price == 100.0
    
    def test_product_with_high_precision_price(self):
        """Test Product with high precision price"""
        product = Product(
            product_id=1,
            name="Precision Product",
            base_price=123.456789
        )
        
        assert product.product_id == 1
        assert product.name == "Precision Product"
        assert product.base_price == 123.456789
    
    def test_product_with_very_large_price(self):
        """Test Product with very large price"""
        large_price = 999999999.99
        product = Product(
            product_id=1,
            name="Expensive Product",
            base_price=large_price
        )
        
        assert product.product_id == 1
        assert product.name == "Expensive Product"
        assert product.base_price == large_price
    
    def test_product_attributes_are_accessible(self):
        """Test that product attributes are directly accessible"""
        product = Product(101, "Test Product", 50.0)
        
        # Test direct attribute access
        assert hasattr(product, 'product_id')
        assert hasattr(product, 'name')
        assert hasattr(product, 'base_price')
        
        # Test attribute modification
        product.product_id = 102
        product.name = "Modified Product"
        product.base_price = 75.0
        
        assert product.product_id == 102
        assert product.name == "Modified Product"
        assert product.base_price == 75.0
    
    def test_product_comparison_by_id(self):
        """Test comparing products by ID"""
        product1 = Product(1, "Product A", 100.0)
        product2 = Product(1, "Product B", 200.0)  # Same ID, different name/price
        product3 = Product(2, "Product A", 100.0)  # Different ID, same name/price
        
        # Products with same ID
        assert product1.product_id == product2.product_id
        
        # Products with different ID
        assert product1.product_id != product3.product_id
    
    def test_product_comparison_by_name(self):
        """Test comparing products by name"""
        product1 = Product(1, "Laptop", 100.0)
        product2 = Product(2, "Laptop", 200.0)  # Same name, different ID/price
        product3 = Product(1, "Desktop", 100.0)  # Same ID/price, different name
        
        # Products with same name
        assert product1.name == product2.name
        
        # Products with different name
        assert product1.name != product3.name
    
    def test_product_comparison_by_price(self):
        """Test comparing products by price"""
        product1 = Product(1, "Product A", 100.0)
        product2 = Product(2, "Product B", 100.0)  # Same price, different ID/name
        product3 = Product(1, "Product A", 200.0)  # Same ID/name, different price
        
        # Products with same price
        assert product1.base_price == product2.base_price
        
        # Products with different price
        assert product1.base_price != product3.base_price
    
    def test_multiple_products_creation(self):
        """Test creating multiple products"""
        products = []
        
        for i in range(5):
            product = Product(
                product_id=i + 1,
                name=f"Product {i + 1}",
                base_price=(i + 1) * 100.0
            )
            products.append(product)
        
        assert len(products) == 5
        
        for i, product in enumerate(products):
            assert product.product_id == i + 1
            assert product.name == f"Product {i + 1}"
            assert product.base_price == (i + 1) * 100.0
    
    def test_product_immutability_concept(self):
        """Test that product attributes can be changed (not immutable)"""
        product = Product(1, "Original", 100.0)
        
        # Verify original values
        assert product.product_id == 1
        assert product.name == "Original"
        assert product.base_price == 100.0
        
        # Modify attributes
        product.product_id = 999
        product.name = "Modified"
        product.base_price = 999.99
        
        # Verify changes
        assert product.product_id == 999
        assert product.name == "Modified"
        assert product.base_price == 999.99


class TestProductEdgeCases:
    """Test edge cases and error conditions for Product class"""
    
    def test_product_with_none_values(self):
        """Test Product creation with None values (should raise errors)"""
        with pytest.raises(TypeError):
            Product(None, "Test", 100.0)
        
        # Name can be None in Python, but may not be desired
        product = Product(1, None, 100.0)
        assert product.name is None
        
        with pytest.raises(TypeError):
            Product(1, "Test", None)
    
    def test_product_with_string_id(self):
        """Test Product creation with string ID (should raise error)"""
        with pytest.raises(TypeError):
            Product("1", "Test", 100.0)
    
    def test_product_with_string_price(self):
        """Test Product creation with string price (should raise error)"""
        with pytest.raises(TypeError):
            Product(1, "Test", "100.0")
    
    def test_product_with_negative_price(self):
        """Test Product with negative price"""
        product = Product(1, "Test", -100.0)
        assert product.base_price == -100.0
        # Note: Business logic might want to prevent negative prices,
        # but the Product class itself doesn't enforce this
    
    def test_product_string_representation(self):
        """Test string representation of Product (if __str__ method exists)"""
        product = Product(1, "Test Product", 123.45)
        
        # Since Product class doesn't define __str__, it will use default
        str_repr = str(product)
        assert "Product" in str_repr  # Should contain class name
        assert "object at" in str_repr  # Default object representation


class TestProductDataTypes:
    """Test various data types with Product class"""
    
    def test_product_id_types(self):
        """Test different numeric types for product_id"""
        # Regular int
        product1 = Product(1, "Test", 100.0)
        assert product1.product_id == 1
        
        # Large int
        large_id = 999999999999
        product2 = Product(large_id, "Test", 100.0)
        assert product2.product_id == large_id
        
        # Zero
        product3 = Product(0, "Test", 100.0)
        assert product3.product_id == 0
    
    def test_product_price_types(self):
        """Test different numeric types for base_price"""
        # Float
        product1 = Product(1, "Test", 100.5)
        assert product1.base_price == 100.5
        
        # Int (should be converted to float)
        product2 = Product(2, "Test", 100)
        assert product2.base_price == 100.0
        assert isinstance(product2.base_price, (int, float))
        
        # Very small float
        product3 = Product(3, "Test", 0.01)
        assert product3.base_price == 0.01
    
    def test_product_name_types(self):
        """Test different string types for name"""
        # Regular string
        product1 = Product(1, "Regular Name", 100.0)
        assert product1.name == "Regular Name"
        
        # Empty string
        product2 = Product(2, "", 100.0)
        assert product2.name == ""
        
        # String with numbers
        product3 = Product(3, "Product 123", 100.0)
        assert product3.name == "Product 123"
        
        # String with whitespace
        product4 = Product(4, "  Spaced Name  ", 100.0)
        assert product4.name == "  Spaced Name  "


if __name__ == "__main__":
    pytest.main([__file__])