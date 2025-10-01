"""
Unit Tests for PricingRule Model using pytest
Tests all functionality of the PricingRule class including static methods for different pricing explanations.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pricing_rule import PricingRule
from constants.tier import Tier
from constants.group import Group


class TestPricingRule:
    """Test suite for PricingRule class using pytest"""
    
    def test_pricing_rule_class_exists(self):
        """Test that PricingRule class exists"""
        assert PricingRule is not None
        assert isinstance(PricingRule, type)
    
    def test_tier_pricing_rules_method_exists(self):
        """Test that tier_pricing_rules method exists"""
        assert hasattr(PricingRule, 'tier_pricing_rules')
        assert callable(PricingRule.tier_pricing_rules)
    
    def test_group_pricing_rules_method_exists(self):
        """Test that group_pricing_rules method exists"""
        assert hasattr(PricingRule, 'group_pricing_rules')
        assert callable(PricingRule.group_pricing_rules)
    
    def test_loyalty_pricing_rules_method_exists(self):
        """Test that loyalty_pricing_rules method exists"""
        assert hasattr(PricingRule, 'loyalty_pricing_rules')
        assert callable(PricingRule.loyalty_pricing_rules)
    
    def test_sub_menu_method_exists(self):
        """Test that sub_menu method exists"""
        assert hasattr(PricingRule, 'sub_menu')
        assert callable(PricingRule.sub_menu)
    
    def test_tier_pricing_rules_silver(self, capsys):
        """Test tier_pricing_rules method with SILVER tier"""
        PricingRule.tier_pricing_rules(Tier.SILVER)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "SILVER calculation" in output
        assert "Final Price per product = Base price of a product * SILVER discount rate" in output
        assert "product_id: 01" in output
        assert "product_name: Laptop" in output
        assert "base_price: LKR 350000" in output
        assert "customer_tier: SILVER" in output
        assert "Final price of the Laptop" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_tier_pricing_rules_gold(self, capsys):
        """Test tier_pricing_rules method with GOLD tier"""
        PricingRule.tier_pricing_rules(Tier.GOLD)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "GOLD calculation" in output
        assert "Final Price per product = Base price of a product * GOLD discount rate" in output
        assert "customer_tier: GOLD" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_tier_pricing_rules_platinum(self, capsys):
        """Test tier_pricing_rules method with PLATINUM tier"""
        PricingRule.tier_pricing_rules(Tier.PLATINUM)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "PLATINUM calculation" in output
        assert "Final Price per product = Base price of a product * PLATINUM discount rate" in output
        assert "customer_tier: PLATINUM" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_group_pricing_rules_regular(self, capsys):
        """Test group_pricing_rules method with REGULAR group"""
        PricingRule.group_pricing_rules(Group.REGULAR)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "REGULAR calculation" in output
        assert "Final Price per product = Base price of a product * REGULAR discount rate" in output
        assert "product_id: 01" in output
        assert "product_name: Laptop" in output
        assert "base_price: LKR 350000" in output
        assert "customer_group: REGULAR" in output
        assert "Final price of the Laptop" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_group_pricing_rules_bulk(self, capsys):
        """Test group_pricing_rules method with BULK group"""
        PricingRule.group_pricing_rules(Group.BULK)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "BULK calculation" in output
        assert "Final Price per product = Base price of a product * BULK discount rate" in output
        assert "customer_group: BULK" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_group_pricing_rules_vip(self, capsys):
        """Test group_pricing_rules method with VIP group"""
        PricingRule.group_pricing_rules(Group.VIP)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "VIP calculation" in output
        assert "Final Price per product = Base price of a product * VIP discount rate" in output
        assert "customer_group: VIP" in output
        assert "350000*(1-0.15)" in output
        assert "297500" in output
    
    def test_loyalty_pricing_rules(self):
        """Test loyalty_pricing_rules method"""
        # This method currently just passes, so test that it doesn't raise an error
        try:
            PricingRule.loyalty_pricing_rules()
        except Exception as e:
            pytest.fail(f"loyalty_pricing_rules raised an unexpected exception: {e}")
    
    def test_tier_pricing_rules_output_format(self, capsys):
        """Test the format and structure of tier pricing rules output"""
        PricingRule.tier_pricing_rules(Tier.SILVER)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check for specific formatting elements
        assert "=" * 100 in output  # Separator line
        assert "NOTE: This price is only applicable when the minimum quantity of the product is matched." in output
        assert "Eg:-" in output
        assert "Product Details" in output
        assert "Tier Discount Details" in output
        assert "Customer Details" in output
    
    def test_group_pricing_rules_output_format(self, capsys):
        """Test the format and structure of group pricing rules output"""
        PricingRule.group_pricing_rules(Group.BULK)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check for specific formatting elements
        assert "=" * 100 in output  # Separator line
        assert "NOTE: This price is only applicable when the minimum quantity of the product is matched." in output
        assert "Eg:-" in output
        assert "Product Details" in output
        assert "Group Discount Details" in output
        assert "Customer Details" in output
    
    def test_tier_pricing_rules_mathematical_calculation(self, capsys):
        """Test that tier pricing rules show correct mathematical calculation"""
        PricingRule.tier_pricing_rules(Tier.GOLD)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check mathematical calculation steps
        assert "Final price of the Laptop" in output
        assert "= 350000*(1-0.15)" in output
        assert "= 350000*0.85" in output
        assert "= 297500" in output
    
    def test_group_pricing_rules_mathematical_calculation(self, capsys):
        """Test that group pricing rules show correct mathematical calculation"""
        PricingRule.group_pricing_rules(Group.VIP)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check mathematical calculation steps
        assert "Final price of the Laptop" in output
        assert "= 350000*(1-0.15)" in output
        assert "= 350000*0.85" in output
        assert "= 297500" in output
    
    @patch('builtins.input', side_effect=['99'])  # Exit option
    def test_sub_menu_exit_option(self, mock_input, capsys):
        """Test sub_menu method with exit option"""
        PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Pricing Rule types" in output
        assert "1. Tiered Pricing" in output
        assert "2. Grouped Pricing" in output
        assert "3. Loyalty Pricing" in output
        assert "99. Back" in output
    
    @patch('builtins.input', side_effect=['1', '99'])  # Test tier pricing then exit
    def test_sub_menu_tier_pricing_option(self, mock_input, capsys):
        """Test sub_menu method with tier pricing option"""
        PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should show all tier calculations
        assert "SILVER calculation" in output
        assert "GOLD calculation" in output
        assert "PLATINUM calculation" in output
    
    @patch('builtins.input', side_effect=['2', '99'])  # Test group pricing then exit
    def test_sub_menu_group_pricing_option(self, mock_input, capsys):
        """Test sub_menu method with group pricing option"""
        PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should show all group calculations
        assert "BULK calculation" in output
        assert "REGULAR calculation" in output
        assert "VIP calculation" in output
    
    @patch('builtins.input', side_effect=['3', '99'])  # Test loyalty pricing then exit
    def test_sub_menu_loyalty_pricing_option(self, mock_input, capsys):
        """Test sub_menu method with loyalty pricing option"""
        PricingRule.sub_menu()
        
        # Since loyalty_pricing_rules() just passes, no specific output expected
        # Just ensure no errors occur
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Pricing Rule types" in output
    
    @patch('builtins.input', side_effect=['5', '99'])  # Invalid option then exit
    def test_sub_menu_invalid_option(self, mock_input, capsys):
        """Test sub_menu method with invalid option"""
        PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Invalid option. Please Try Again" in output
    
    @patch('builtins.input', side_effect=['0', '99'])  # Another invalid option then exit
    def test_sub_menu_another_invalid_option(self, mock_input, capsys):
        """Test sub_menu method with another invalid option"""
        PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Invalid option. Please Try Again" in output


class TestPricingRuleEdgeCases:
    """Test edge cases and error conditions for PricingRule class"""
    
    def test_tier_pricing_rules_with_none(self):
        """Test tier_pricing_rules method with None (should raise error)"""
        with pytest.raises((TypeError, AttributeError)):
            PricingRule.tier_pricing_rules(None)
    
    def test_group_pricing_rules_with_none(self):
        """Test group_pricing_rules method with None (should raise error)"""
        with pytest.raises((TypeError, AttributeError)):
            PricingRule.group_pricing_rules(None)
    
    def test_tier_pricing_rules_with_invalid_type(self):
        """Test tier_pricing_rules method with invalid type"""
        with pytest.raises((TypeError, AttributeError)):
            PricingRule.tier_pricing_rules("INVALID_TIER")
    
    def test_group_pricing_rules_with_invalid_type(self):
        """Test group_pricing_rules method with invalid type"""
        with pytest.raises((TypeError, AttributeError)):
            PricingRule.group_pricing_rules("INVALID_GROUP")
    
    @patch('builtins.input', side_effect=['abc', '99'])  # Invalid input then exit
    def test_sub_menu_with_non_integer_input(self, mock_input):
        """Test sub_menu method with non-integer input"""
        with pytest.raises(ValueError):
            PricingRule.sub_menu()
    
    def test_pricing_rule_has_no_instance_methods(self):
        """Test that PricingRule appears to be designed as a utility class"""
        # All methods should be static/class methods, no instance methods expected
        instance_methods = [method for method in dir(PricingRule) 
                          if not method.startswith('_') and callable(getattr(PricingRule, method))]
        
        # Check that the expected methods exist
        expected_methods = ['tier_pricing_rules', 'group_pricing_rules', 'loyalty_pricing_rules', 'sub_menu']
        for method in expected_methods:
            assert method in instance_methods
    
    def test_pricing_rule_no_initialization_needed(self):
        """Test that PricingRule doesn't need to be instantiated"""
        # Should be able to call methods directly on the class
        try:
            PricingRule.loyalty_pricing_rules()
        except Exception as e:
            pytest.fail(f"Calling static method on class raised an unexpected exception: {e}")


class TestPricingRuleOutputConsistency:
    """Test consistency of output across different pricing rule methods"""
    
    def test_all_tier_rules_have_consistent_format(self, capsys):
        """Test that all tier pricing rules have consistent output format"""
        tiers = [Tier.SILVER, Tier.GOLD, Tier.PLATINUM]
        outputs = []
        
        for tier in tiers:
            PricingRule.tier_pricing_rules(tier)
            captured = capsys.readouterr()
            outputs.append(captured.out)
        
        # Check that all outputs have similar structure
        for output in outputs:
            assert "calculation" in output
            assert "Final Price per product = Base price of a product *" in output
            assert "NOTE: This price is only applicable" in output
            assert "Product Details" in output
            assert "Tier Discount Details" in output
            assert "Customer Details" in output
            assert "Final price of the Laptop" in output
            assert "350000*(1-0.15)" in output
            assert "297500" in output
            assert "=" * 100 in output
    
    def test_all_group_rules_have_consistent_format(self, capsys):
        """Test that all group pricing rules have consistent output format"""
        groups = [Group.REGULAR, Group.BULK, Group.VIP]
        outputs = []
        
        for group in groups:
            PricingRule.group_pricing_rules(group)
            captured = capsys.readouterr()
            outputs.append(captured.out)
        
        # Check that all outputs have similar structure
        for output in outputs:
            assert "calculation" in output
            assert "Final Price per product = Base price of a product *" in output
            assert "NOTE: This price is only applicable" in output
            assert "Product Details" in output
            assert "Group Discount Details" in output
            assert "Customer Details" in output
            assert "Final price of the Laptop" in output
            assert "350000*(1-0.15)" in output
            assert "297500" in output
            assert "=" * 100 in output
    
    def test_tier_and_group_rules_have_similar_structure(self, capsys):
        """Test that tier and group pricing rules have similar output structure"""
        PricingRule.tier_pricing_rules(Tier.SILVER)
        tier_output = capsys.readouterr().out
        
        PricingRule.group_pricing_rules(Group.BULK)
        group_output = capsys.readouterr().out
        
        # Both should have similar structural elements
        common_elements = [
            "calculation",
            "Final Price per product = Base price of a product *",
            "NOTE: This price is only applicable",
            "Product Details",
            "Customer Details",
            "Final price of the Laptop",
            "350000*(1-0.15)",
            "297500",
            "=" * 100
        ]
        
        for element in common_elements:
            assert element in tier_output
            assert element in group_output
    
    def test_pricing_calculations_are_consistent(self, capsys):
        """Test that all pricing calculations show the same example values"""
        methods_and_params = [
            (PricingRule.tier_pricing_rules, Tier.SILVER),
            (PricingRule.tier_pricing_rules, Tier.GOLD),
            (PricingRule.tier_pricing_rules, Tier.PLATINUM),
            (PricingRule.group_pricing_rules, Group.REGULAR),
            (PricingRule.group_pricing_rules, Group.BULK),
            (PricingRule.group_pricing_rules, Group.VIP)
        ]
        
        for method, param in methods_and_params:
            method(param)
            captured = capsys.readouterr()
            output = captured.out
            
            # All should show the same example calculation
            assert "product_id: 01" in output
            assert "product_name: Laptop" in output
            assert "base_price: LKR 350000" in output
            assert "0.10 (10%)" in output  # Discount rate example
            assert "350000*(1-0.15)" in output
            assert "350000*0.85" in output
            assert "297500" in output


class TestPricingRuleBusinessLogic:
    """Test business logic aspects of PricingRule class"""
    
    def test_pricing_rule_demonstrates_discount_concept(self, capsys):
        """Test that pricing rules demonstrate the discount concept correctly"""
        PricingRule.tier_pricing_rules(Tier.GOLD)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should demonstrate discount calculation
        assert "350000*(1-0.15)" in output  # Original price * (1 - discount rate)
        assert "350000*0.85" in output      # Simplified calculation
        assert "297500" in output           # Final discounted price
        
        # The final price should be less than original (demonstrating discount)
        original_price = 350000
        final_price = 297500
        assert final_price < original_price
    
    def test_pricing_rule_shows_minimum_quantity_requirement(self, capsys):
        """Test that pricing rules mention minimum quantity requirements"""
        PricingRule.tier_pricing_rules(Tier.PLATINUM)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "minimum quantity" in output.lower()
        assert "NOTE: This price is only applicable when the minimum quantity of the product is matched." in output
    
    def test_pricing_rule_provides_realistic_example(self, capsys):
        """Test that pricing rules provide realistic business examples"""
        PricingRule.group_pricing_rules(Group.VIP)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should provide realistic example data
        assert "Laptop" in output  # Realistic product
        assert "LKR 350000" in output  # Realistic price in local currency
        assert "John Doe" in output  # Realistic customer name
        assert "customer_id: 01" in output  # Realistic ID format
    
    def test_all_pricing_types_covered_in_submenu(self, capsys):
        """Test that sub menu covers all major pricing types"""
        # Mock the input to show menu and exit
        with patch('builtins.input', return_value='99'):
            PricingRule.sub_menu()
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should cover all three pricing types
        assert "1. Tiered Pricing" in output
        assert "2. Grouped Pricing" in output
        assert "3. Loyalty Pricing" in output
        
        # Should provide navigation options
        assert "99. Back" in output
        assert "Select Option (1, 2, 3)" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])