class CreditCardDecorator:
    def __init__(self, credit_card):
        self.credit_card = credit_card

    def give_details(self):
        return self.credit_card.give_details()


class GoldenCreditCard(CreditCardDecorator):
    def give_details(self):
        details = super().give_details()
        details["benefits"] = "5% cashback on all purchases"
        return details


class CorporateCreditCard(CreditCardDecorator):
    def give_details(self):
        details = super().give_details()
        details["benefits"] = "Higher credit limit for businesses"
        return details


class VIPCustomer:
    def __init__(self, customer):
        self.customer = customer

    def give_details(self):
        details = self.customer.give_details()
        details["vip_status"] = "Priority customer support and exclusive offers"
        return details
