from credit_card import CreditCard
from personal_info import PersonalInfo
from bank_info import BankInfo
from bank_customer import BankCustomer
from dekorators import VIPCustomer, GoldenCreditCard

def main():
    # Create CreditCard object
    credit_card = CreditCard("John Doe", "1234-5678-9012-3456", 5000, 30, "123")
    golden_card = GoldenCreditCard(credit_card)

    # Create PersonalInfo and BankInfo objects
    personal_info = PersonalInfo(name="John Doe", age=30, address="123 Elm Street")
    bank_info = BankInfo("Big Bank", "John Doe")
    bank_info.accounts_number.append(credit_card.account_number)

    # Create BankCustomer and VIPCustomer objects
    bank_customer = BankCustomer(personal_info, bank_info)
    vip_customer = VIPCustomer(bank_customer)

    # Display results
    print("Credit Card Details:", golden_card.give_details())
    print("Bank Customer Details:", vip_customer.give_details())

if __name__ == "__main__":
    main()
