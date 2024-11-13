class Customer:
    def __init__(self, ID, name, age, operator, bill, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operator = operator
        self.bill = bill
        self.limitingAmount = limitingAmount

    def talk(self, minute, other):
        cost = self.operator.calculateTalkingCost(minute, self)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f'{self.name} talked to {other.name} for {minute} minutes.')
        else:
            print(f'{self.name} cannot talk due to bill limit.')

    def message(self, quantity, other):
        cost = self.operator.calculateMessageCost(quantity, self, other)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f'{self.name} sent {quantity} messages to {other.name}.')
        else:
            print(f'{self.name} cannot send messages due to bill limit.')

    def connection(self, amount):
        cost = self.operator.calculateNetworkCost(amount)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f'{self.name} connected to the internet using {amount} MB.')
        else:
            print(f'{self.name} cannot connect due to bill limit.')

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age


class Operator:
    def __init__(self, ID, talkingCharge, messageCost, networkCharge, discountRate):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute, customer):
        cost = minute * self.talkingCharge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateMessageCost(self, quantity, customer, other):
        cost = quantity * self.messageCost
        if customer.operator.ID == other.operator.ID:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateNetworkCost(self, amount):
        return amount * self.networkCharge

class Bill:
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount):
        return (self.currentDebt + amount) <= self.limitingAmount

    def add(self, amount):
        self.currentDebt += amount

    def pay(self, amount):
        self.currentDebt -= amount

    def changeTheLimit(self, amount):
        self.limitingAmount = amount

    def getCurrentDebt(self):
        return self.currentDebt

    def getLimitingAmount(self):
        return self.limitingAmount
        
class Main:
    def __init__(self):
        self.customers = []
        self.operators = []
        self.bills = []

    def create_customer(self, ID, name, age, operator, bill, limitingAmount):
        customer = Customer(ID, name, age, operator, bill, limitingAmount)
        self.customers.append(customer)

    def create_operator(self, ID, talkingCharge, messageCost, networkCharge, discountRate):
        operator = Operator(ID, talkingCharge, messageCost, networkCharge, discountRate)
        self.operators.append(operator)

    def create_bill(self, limitingAmount):
        bill = Bill(limitingAmount)
        self.bills.append(bill)

    def find_customer(self, ID):
        for customer in self.customers:
            if customer.ID == ID:
                return customer
        return None

    def find_operator(self, ID):
        for operator in self.operators:
            if operator.ID == ID:
                return operator
        return None

    def run(self):
        print("Communication System Simulation")

        self.create_operator(0, 1.5, 0.5, 0.2, 10)
        self.create_operator(1, 1.2, 0.6, 0.3, 15)

        bill1 = Bill(100)
        bill2 = Bill(150)

        self.create_customer(0, "Alice", 20, self.operators[0], bill1, 100)
        self.create_customer(1, "Bob", 16, self.operators[1], bill2, 150)

        customer1 = self.find_customer(0)
        customer2 = self.find_customer(1)

        customer1.talk(10, customer2)
        
        customer2.message(5, customer1)
        
        customer1.connection(50)

        customer2.connection(200)


if __name__ == "__main__":
    main_program = Main()
    main_program.run()