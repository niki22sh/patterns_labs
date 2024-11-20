class BankInfo:
    def __init__(self, bank_name, holder_name):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = []
        self.credit_history = {}

    def transaction_list(self, account_number):
        return [f"Transaction {i+1} for {account_number}" for i in range(3)]
