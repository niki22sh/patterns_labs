from bank_info import BankInfo
from personal_info import PersonalInfo

class BankCustomer:
    def __init__(self, personal_info, bank_details):
        self.personal_info = personal_info
        self.bank_details = bank_details

    def give_details(self):
        details = {
            "personal_info": vars(self.personal_info),
            "bank_details": {
                "bank_name": self.bank_details.bank_name,
                "holder_name": self.bank_details.holder_name,
                "accounts_number": self.bank_details.accounts_number,
            },
            "transactions": self.bank_details.transaction_list(self.bank_details.accounts_number[0]) if self.bank_details.accounts_number else []
        }
        return details
