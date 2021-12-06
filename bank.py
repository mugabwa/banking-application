class Bank:
    def __init__(self) -> None:
        self.Users = dict()
        self.Accounts = dict()
        self.transact = list()

    def createAcccount(self,userInfo:dict,accountInfo:dict):
        for k in userInfo.keys():
            if k in self.Users.keys():
                return False 
        self.Users.update(userInfo)
        self.Accounts.update(accountInfo)
        return True
    def deposit(self,accountNo, amount):
        if accountNo in self.Accounts.keys():
            self.Accounts[accountNo]['balance'] += int(amount)
            return True
    def withdraw(self,accountNo, amount):
        if accountNo in self.Accounts:
            if self.Accounts[accountNo]['balance'] >= int(amount):
                self.Accounts[accountNo]['balance'] -= int(amount)
                return True
            else:
                return False
    def checkBalance(self,accountNo):
        if accountNo in accountNo:
            return self.Accounts[accountNo]['balance']
    def transaction(self,usr,action,amount = 0):
        if action == "checked balance":
            log = [usr,"{nm} account number {id} {act}".format(nm=self.Accounts[usr]['Name'],
            id=usr,act=action)]
        else:
            log = [usr,"{nm} account number {id} {act} {amt}".format(nm=self.Accounts[usr]['Name'],
            id=usr,act=action,amt=amount)]
        self.transact.append(log)

    def transactionHistory(self):
        return self.transact
