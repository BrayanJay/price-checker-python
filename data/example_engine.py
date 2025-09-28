import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.customer import Customer
from constants.group import Group
from constants.tier import Tier
from models.product import Product
from models.place_order import PlaceOrder
from price_hierarchy.group_prices import GroupedPrices
from price_hierarchy.tiered_prices import TieredPrices
from price_hierarchy.loyalty_prices import LoyaltyPrices


class ExampleEngine:

    #Initiating sample customers

    customer1 = Customer(
        customer_id=1,
        name="Alice",
        tier=Tier.GOLD,
        groups=[Group.REGULAR, Group.VIP]
    )

    customer2 = Customer(
        customer_id=2,
        name="Bob",
        tier=Tier.SILVER,
        groups=[Group.BULK]
    )

    customer3 = Customer(
        customer_id=3,
        name="Charlie",
        tier=  Tier.PLATINUM,
        groups=[Group.VIP]
    )

    customer4 = Customer(
        customer_id=4,
        name="David",
        tier=Tier.SILVER,
        groups=[Group.BULK]
    )

    #Initiating sample products

    product1 = Product(
        product_id=1,
        name="Laptop",
        base_price=350000
    )

    product2 = Product(
        product_id=2,
        name="Smartphone",
        base_price=200000
    )

    product3 = Product(
        product_id=3,
        name="Tablet",
        base_price=150000
    )

    product4 = Product(
        product_id=4,
        name="Smartwatch",
        base_price=100000
    )

    #Initiating sample pricing rules

    #TIER PRICING

    tier1 = TieredPrices(
        product=product1,
        tier=Tier.GOLD,
        discount_rate=0.15,
        min_qty=4
    )
    TieredPrices.add_tiered_price(tier1)

    tier2 = TieredPrices(
        product=product1,
        tier=Tier.SILVER,
        discount_rate=0.05,
        min_qty=5
    )
    TieredPrices.add_tiered_price(tier2)

    tier3 = TieredPrices(
        product=product1,
        tier=Tier.PLATINUM,
        discount_rate=0.40,
        min_qty=2
    )
    TieredPrices.add_tiered_price(tier3)

    #GROUP PRICING

    group1 = GroupedPrices(
        product=product1,
        group=Group.REGULAR,
        discount_rate=0.20,
        min_qty=5
    )
    GroupedPrices.add_grouped_price(group1)

    group2 = GroupedPrices(
        product=product1,
        group=Group.BULK,
        discount_rate=0.10,
        min_qty=10
    )
    GroupedPrices.add_grouped_price(group2)

    group3 = GroupedPrices(
        product=product1,
        group=Group.VIP,
        discount_rate=0.50,
        min_qty=2
    )
    GroupedPrices.add_grouped_price(group3)

    #LOYALTY PRICING

    loyalty1 = LoyaltyPrices(
        product=product2,
        customer=customer1,
        discount_rate=0.20,
        min_qty=5
    )
    LoyaltyPrices.add_loyalty_price(loyalty1)

    loyalty2 = LoyaltyPrices(
        product=product1,
        customer=customer1,
        discount_rate=0.10,
        min_qty=10
    )
    LoyaltyPrices.add_loyalty_price(loyalty2)

    loyalty3 = LoyaltyPrices(
        product=product3,
        customer=customer1,
        discount_rate=0.50,
        min_qty=2
    )
    LoyaltyPrices.add_loyalty_price(loyalty3)

    #ORDERS

    order1 = PlaceOrder(
        product_id=1,
        customer_id=1,
        quantity=5
    )
    PlaceOrder.append_order(order1)

    order2 = PlaceOrder(
        product_id=1,
        customer_id=2,
        quantity=10
    )
    PlaceOrder.append_order(order2)

    order3 = PlaceOrder(
        product_id=3,
        customer_id=1,
        quantity=1
    )
    PlaceOrder.append_order(order3)

    print("Loyalty Prices:")
    print(LoyaltyPrices.get_loyalty_prices())
    print("\n")
    print("Tiered Prices:")
    print(TieredPrices.get_tiered_prices())
    print("\n")
    print("Grouped Prices:")
    print(GroupedPrices.get_grouped_prices())
    print("\n")
    print("Placed Orders:")
    print(PlaceOrder.view_orders())