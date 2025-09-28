from models.customer import Customer
from constants.group import Group
from constants.tier import Tier

class PricingEngine:

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

    print(customer1)