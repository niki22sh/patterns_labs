import hashlib

class CreditCard:
    def __init__(self, client, account_number, credit_limit, grace_period, cvv):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self._cvv = self.encrypt(cvv)

    def encrypt(self, value):
        return hashlib.sha256(value.encode()).hexdigest()

    def decrypt(self, value):
        raise NotImplementedError("Cannot decrypt a hash!")

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value):
        self._cvv = self.encrypt(value)

    def give_details(self):
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self._cvv,
        }
