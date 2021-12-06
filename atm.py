from tkinter.constants import BOTH, BOTTOM, CENTER, LEFT, N, TOP
from tkinter.font import BOLD
import bank
import tkinter as tk
from tkinter import messagebox

class Globals:
    user_acc = None
    sec_code = None
    amount = None
    message = ''
    damount = None

message = ''

class ATM:
    def __init__(self, Bank) -> None:
        self.Bank = Bank
        self.is_verfied = False
        self.current_user = None
    def verify(self):
        user = Globals.user_acc.get()
        secCode = Globals.sec_code.get()
        print(user," ",secCode)
        if user in self.Bank.Users and secCode == self.Bank.Users[user]:
            self.is_verfied = True
            self.current_user = user
            return True
        return False
    def deposit(self,amount):
        if not self.is_verfied:
            self.verify()
        if self.is_verfied:
            if(self.Bank.deposit(self.current_user,amount)):
                self.Bank.transaction(self.current_user,"deposit", amount)
            return True
        return False

    def withdraw(self, amount):
        if not self.is_verfied:
            self.verify()
        if self.is_verfied and self.Bank.withdraw(self.current_user,amount):
            self.Bank.transaction(self.current_user,"withdrew", amount)
            return amount
        return False

    def checkBalance(self):
        if not self.is_verfied:
            self.verify()
        if self.is_verfied:
            amount = self.Bank.checkBalance(self.current_user)
            if amount:
                self.Bank.transaction(self.current_user,"checked balance",)
                return amount
        return False
    
    def transactionHistory(self):
        return self.Bank.transactionHistory()
    
    def closeTransaction(self):
        self.is_verfied = False
        self.current_user = None

class tkinterApp(tk.Tk):
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        tk.Tk.__init__(self, *args, **kwargs)
        Globals.amount = tk.StringVar()
        Globals.damount = tk.StringVar()
        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainPage, VerificationPage, OptionPage, DepositPage, WithdrawPage,TransactionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky='nsew')
        self.show_frame(MainPage)
    
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

    def verify(self):
        if(self.obj.verify()):
            self.show_frame(OptionPage)
    
    def close(self):
        self.obj.closeTransaction()
        self.show_frame(MainPage)

    def getmsg(self):
        global message
        return message
        return Globals.message

    def transactions(self,opt):
        global message
        if opt == 'deposit':
            # print(Globals.damount.get())
            self.obj.deposit(Globals.damount.get())
            message = "You have successfuly deposited {}".format(Globals.damount.get())
            self.show_frame(TransactionPage)
            print(self.getmsg())
        # elif opt == 'withdraw':
        #     if(self.obj.withdraw(Globals.amount.get())):
        #         Globals.message = "You have successfuly withdrawn {}".format(Globals.amount.get())
        #     else:
        #         Globals.message = "Error! Withdrawal of {} failed".format(Globals.amount.get())
        #     self.show_frame(TransactionPage)
        # elif opt == 'balance':
        #     Globals.message = "You account balance is {}".format(self.obj.checkBalance())
        #     self.show_frame(TransactionPage)
        # elif opt == 'history':
        #     if(self.obj.transactionHistory()):
        #         for x in self.obj.transactionHistory():
        #             Globals.message += x[1]
        #             Globals.message += '\n'
        #         print('xx ',Globals.message)
        #     else:
        #         Globals.message = "Error! Transaction history is empty!"
        #     self.show_frame(TransactionPage)



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Main Page")
        label.grid(row=0, columnspan=3, padx=5, pady=5)
        btn1 = tk.Button(self,text="Perform Transaction",command=lambda:controller.show_frame(VerificationPage))
        btn1.grid(row=2,column=1,padx=5,pady=10)
        txt = tk.Text(self, height=5)
        txt.grid(row=1,columnspan=3,padx=5, pady=5)
        message = """Welcome to Equity Bank, a world class bank.
We would like to provide the best experience for our customers.
Thank you for chosing to bank with us.
For any complaints, visit our website and give your feedback."""

        txt.insert(tk.END, message)


class VerificationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        Globals.user_acc = tk.StringVar()
        Globals.sec_code = tk.StringVar()
        label = tk.Label(self, text="Login Page")
        label.grid(row=0, columnspan=2, padx=5, pady=5)
        label_acc = tk.Label(self, text="Account Number")
        label_acc.grid(row=1, column=0, padx=5, pady=5)
        acc = tk.Entry(self,textvariable=Globals.user_acc)
        acc.grid(row=1,column=1,padx=5,pady=5)
        label_sec = tk.Label(self, text="Security Code")
        label_sec.grid(row=2, column=0, padx=5, pady=5)
        sec = tk.Entry(self,textvariable=Globals.sec_code)
        sec.grid(row=2,column=1,padx=5,pady=5)
        btn1 = tk.Button(self,text="Login",command=lambda:controller.verify())
        btn1.grid(row=3,column=1,padx=5,pady=5)

        btn1 = tk.Button(self,text="Back",command=lambda:controller.close())
        btn1.grid(row=3,column=0,padx=5,pady=5) 
        # btn1 = tk.Button(self,text="Page 2",command=lambda:controller.show_frame(Page2))
        # btn1.grid(row=2,column=1,padx=5,pady=5) 
        

class OptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Options Page")
        label.grid(row=0, columnspan=3, padx=5, pady=5)
        btn1 = tk.Button(self,text="Deposit Cash",command=lambda:controller.show_frame(DepositPage))
        btn1.grid(row=1,column=0,padx=5,pady=5)
        btn1 = tk.Button(self,text="Withdraw Cash",command=lambda:controller.show_frame(WithdrawPage))
        btn1.grid(row=1,column=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Check Balance",command=lambda:controller.transactions('balance'))
        btn1.grid(row=2,column=0,padx=5,pady=5)
        btn1 = tk.Button(self,text="Transaction History",command=lambda:controller.transactions('history'))
        btn1.grid(row=2,column=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Return To Main Page",command=lambda:controller.close())
        btn1.grid(row=3,column=1,padx=5,pady=5) 

class DepositPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Deposit Page")
        label.grid(row=0,columnspan=3, padx=5, pady=5)
        label_amnt = tk.Label(self, text="Deposit Amount")
        label_amnt.grid(row=1, column=0, padx=5, pady=5)
        amnt = tk.Entry(self,textvariable=Globals.damount)
        amnt.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Deposit",command=lambda:controller.transactions('deposit'))
        btn1.grid(row=2,column=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Return To Main Page",command=lambda:controller.close())
        btn1.grid(row=2,column=0,padx=5,pady=5) 

class WithdrawPage(tk.Frame):
    def __init__(self, parent, controller):
        Globals.amount = tk.StringVar()
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Withdrawal Page")
        label.grid(row=0, columnspan=3, padx=5, pady=5)
        label_amnt = tk.Label(self, text="Withdrawal Amount")
        label_amnt.grid(row=1, column=0, padx=5, pady=5)
        amnt = tk.Entry(self,textvariable=Globals.amount)
        amnt.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Withdraw",command=lambda:controller.transactions('withdraw'))
        btn1.grid(row=2,column=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Return To Main Page",command=lambda:controller.close())
        btn1.grid(row=2,column=0,padx=5,pady=5)

class TransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        global message
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Transaction Page")
        label.grid(row=0, columnspan=3, padx=5, pady=5)
        txt = tk.Text(self, height=5)
        txt.grid(row=1,columnspan=3,padx=5, pady=5)
        btn1 = tk.Button(self,text="OK",command=lambda:controller.show_frame(OptionPage))
        btn1.grid(row=2,column=2,padx=5,pady=5)
        btn1 = tk.Button(self,text="Return To Main Page",command=lambda:controller.close())
        btn1.grid(row=2,column=0,padx=5,pady=5)
        txt.insert(tk.END, controller.getmsg())
        print('1', message)

def main():
    users = {"12345":"password","67890":"password1","92304":"password2"}
    acc = {"12345":{"Name":"Mark Odhis","balance":2000},
    "67890":{"Name":"Amos Moth","balance":4000},
    "92304":{"Name":"Ann Washa","balance":5000}}
    Equity = bank.Bank()
    Equity.createAcccount(users,acc)
    branch1 = ATM(Equity)
    app = tkinterApp(obj=branch1)
    app.geometry("660x550")
    app.title("Equity Bank ATM")
    app.mainloop()


if __name__ == "__main__":
    main()