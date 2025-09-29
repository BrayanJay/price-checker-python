import sys
import os

from constants.price import PriceType

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def find_all_applicable_prices_for_order(order: dict, products: list[dict], customers: list[dict]) -> dict:

    base_price = 0
    applicable_loyalty_price = 0
    applicable_tiered_price = 0
    applicable_grouped_prices = []
    
    # Find the product
    product = next((p for p in products if p["product_id"] == order["product_id"]), None)
    if not product:
        raise ValueError("Product not found")
    base_price = product["base_price"]

    # Find the customer
    customer = next((c for c in customers if c["customer_id"] == order["customer_id"]), None)
    if not customer:
        raise ValueError("Customer not found")

    # Check loyalty prices (customer-specific prices)
    if "loyalty_products" in customer:
        for loyalty_product in customer["loyalty_products"]:
            if (loyalty_product["customer_id"] == order["customer_id"] and 
                loyalty_product["product_id"] == order["product_id"] and 
                order["quantity"] >= loyalty_product["min_qty"]):
                applicable_loyalty_price = base_price * (1 - loyalty_product["discount_rate"])
                break

    # Check tiered prices (customer tier-based prices)
    if "tier_prices" in product:
        for tier_price in product["tier_prices"]:
            if (tier_price["product_id"] == order["product_id"] and 
                order["quantity"] >= tier_price["min_qty"] and 
                customer["tier"] == tier_price["tier"]):
                applicable_tiered_price = base_price * (1 - tier_price["discount_rate"])
                break

    # Check group prices (customer group-based prices)
    if "group_prices" in product:
        for group_price in product["group_prices"]:
            if (group_price["product_id"] == order["product_id"] and 
                order["quantity"] >= group_price["min_qty"]):

                if group_price["group"] in customer["groups"]:
                    applicable_grouped_prices.append({
                        "group": group_price["group"],
                        "price": base_price * (1 - group_price["discount_rate"])
                    })
                            
    return {
        "base_price": base_price, 
        "loyalty_price": applicable_loyalty_price, 
        "tier_price": applicable_tiered_price, 
        "group_prices": applicable_grouped_prices
    }


def find_best_applicable_price(orders: list[dict], products: list[dict], customers: list[dict]) -> list[dict]:

    results = []
    
    for order in orders:
        try:
            price_options = find_all_applicable_prices_for_order(order, products, customers)
            
            # To Collect all applicable prices with their types
            applicable_prices = []
            
            if price_options["loyalty_price"] > 0:
                applicable_prices.append((PriceType.CUSTOMER, price_options["loyalty_price"]))
            
            if price_options["tier_price"] > 0:
                applicable_prices.append((PriceType.TIER, price_options["tier_price"]))

            for group_price in price_options["group_prices"]:
                applicable_prices.append((PriceType.GROUP, group_price["price"]))

            applicable_prices.append((PriceType.NORMAL, price_options["base_price"]))

            # Find the best price
            best_price_type, best_price = min(applicable_prices, key=lambda x: x[1])
            
            # Format product ID as requested (P + zero-padded ID)
            product_id_formatted = f"P{order['product_id']:03d}"
            
            results.append({
                "product_id": product_id_formatted,
                "price": best_price,
                "price_type": best_price_type
            })
            
        except ValueError as e:
            # Handle cases where product or customer not found
            product_id_formatted = f"P{order['product_id']:03d}"
            results.append({
                "product_id": product_id_formatted,
                "price": 0,
                "price_type": "ERROR"
            })
    
    return results