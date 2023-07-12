from datetime import datetime
import time


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def initial_deposit(self):
        while True:
            try:
                amount = int(input('Enter amount of Deposit:'))
                self.balance += amount
                print('The Amount is successfully deposited into your Account.\n')
                break
            except ValueError:
                print('Invalid Input!')
                print('Try Again\n')

    def withdraw(self):
        amount = int(input('Enter amount of withdrawal:'))
        if self.balance >= amount:
            self.balance -= amount
            print('The Amount is successfully withdrawn from your Account.')
        else:
            print("Withdrawal isn't possible.")

    def balance_enquiry(self):
        print(f'The current balance in your Account is Rs.{self.balance}\n')


class CheckingAccount(Account):
    def __init__(self, account, credit_limit: int = 3000, user=' '):
        super().__init__(account.balance)
        self.credit_limit = credit_limit
        self.user = user

    def user_credit (self):
        print(f'We provide a credit limit of Rs.{self.credit_limit} with an overdraft fee of Rs.500.\n')
        while True:

            try:
                withdraw = int(input('Enter Amount to Withdraw Money from Account:'))
                break

            except ValueError:
                print('Invalid Input!')
                print('Try Again\n')

        if withdraw <= self.balance:
            self.balance -= withdraw
            print(f'Withdrawal of Amount {withdraw} is successfully completed!\n')
            with open('data.txt', 'r+') as file:
                data = file.readlines()

                for index, line in enumerate(data):
                    temp_user = line.strip().split(',')
                    if self.user == temp_user[3]:
                        temp_user[5] = str(self.balance)
                        data[index] = (",".join(temp_user) + "\n")
                        with open(self.user + ".txt", "a") as user_file:
                            user_file.write('CASH WITHDRAWAL,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +','+ str(withdraw) + '\n')

                        with open('GENERALIZED HISTORY.txt', "a") as user_file:
                            user_file.write(self.user+' :CASH WITHDRAWAL,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                            + ',' + str(withdraw) + '\n')

            with open('data.txt', "w") as f:
                for line in data:
                    f.write(line)

        elif withdraw <= (self.balance + self.credit_limit):
            print('You do not have sufficient balance, so it will deduct from the credit limit.')
            print('And for this, the overdraft fee is Rs.500')
            amount = self.balance + self.credit_limit
            self.balance = self.balance - (amount + 500)
            amount -= withdraw
            print(f'Withdrawal of Amount {withdraw} is successfully completed with an overdraft fee of Rs.500\n')

        else:
            print('Withdrawal is not possible as you are exceeding the credit limit of the bank.\n')

    def deposit_amount(self):
        deposit = abs(int(input('Enter Amount to Deposit Money to the Account:')))
        self.balance += deposit
        with open('data.txt', 'r+') as file:
            data = file.readlines()

            for index, line in enumerate(data):
                temp_user = line.strip().split(',')
                if self.user == temp_user[3]:
                    temp_user[5] = str(self.balance)
                    data[index] = (",".join(temp_user) + "\n")

                    with open(self.user + ".txt", "a") as user_file:
                        user_file.write('CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',' + str(deposit) + '\n')

                    with open('GENERALIZED HISTORY.txt', "a") as hist_file:
                        hist_file.write(self.user + ' :CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                        + ',' + str(deposit) + '\n')

        with open('data.txt', "w") as f:
            for line in data:
                f.write(line)


class SavingAccount(Account):
    def __init__(self, account, interest=12):
        super().__init__(account.balance)
        self.interest_rate = interest

    def user_credit(self):
        print(f'We provide a 12% interest rate for our customers.\n')
        interest = (self.interest_rate / 100) * self.balance
        print(f'You have got a monthly interest of Rs.{interest}.')
        self.balance += interest
        time.sleep(1)
        print(f'Monthly Interest is Successfully added into your Account.\n')
        print(f'Your current balance is Rs.{self.balance}.')


class LoanAccount(Account):
    def __init__(self, account, principal_amount=0, interest=15, loan_dur=0):
        super().__init__(account.balance)
        self.principal_amount = principal_amount
        self.interest_rate = interest
        self.loan_duration = loan_dur

    def user_credit(self):
        print('We got you covered! Our bank provides loans for your needs, but it has some conditions.')
        print('We have an interest rate of 15% for any amount you want.\n')
        self.principal_amount = int(input('Enter amount for the loan:'))
        self.interest_rate = int(15)
        self.loan_duration = int(input('Enter the duration of the loan in months:'))
        print(
            f'You demand an amount for the loan Rs.{self.principal_amount} and settle for the duration of {self.loan_duration} months.')
        loan = (self.interest_rate / 100) * self.principal_amount
        loan = loan + self.principal_amount
        result = loan / self.loan_duration
        print(f'You have to pay the bank Rs.{round(result, 1)} monthly for {self.loan_duration} months.')


class Customer:
    def __init__(self, f_name='None', l_name='None', address='None', username='None', password='None'):
        self.first_Name = f_name
        self.last_Name = l_name
        self.address = address
        self.username = username
        self.password = password
        self.account = None

    def create_account(self):
        with open('data.txt', 'r') as file:
            usernames = set(line.strip().split(',')[3] for line in file)

        with open('data.txt', 'a') as file:
            self.first_Name = input('Enter your first name:')
            self.last_Name = input('Enter your last name:')
            self.address = input('Enter your Address for Basic Information:')
            while True:
                self.username = input('Choose a Username for your Bank Account:')
                if self.username in usernames:
                    print('Username is already taken. Try another username.')
                else:
                    break
            self.password = input('Choose a Password for your Bank Account:')
            self.account = Account()
            self.account.initial_deposit()
            self.account.balance_enquiry()
            file.write(
                f'{self.first_Name},{self.last_Name},{self.address},{self.username},{self.password},{self.account.balance}\n')
            time.sleep(1.5)

            with open(self.username+".txt", "w") as user_file:
                user_file.write('ACCOUNT CREATED,'+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+',None'+'\n')

            with open('GENERALIZED HISTORY.txt', "a") as hist_file:
                hist_file.write(self.username+' :ACCOUNT CREATED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                                ',None' + '\n')


    def reg_account(self):
        while True:
            self.username = input('Enter your Username:')
            self.password = input('Enter your Password:')

            with open('data.txt', 'r') as file:

                for line in file:
                    data = line.strip().split(',')

                    if self.username == data[3] and self.password == data[4]:
                        with open(self.username + ".txt", "a") as user_file:
                            user_file.write('SIGNED IN,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',None' + '\n')

                        print()
                        print(f'Welcome Back {data[0]} {data[1]}\n')
                        self.account = Account(int(data[5]))
                        print(f'You have a current balance of {data[5]}\n')
                        return
            print('Invalid username or password. Please try again.\n')


print('Press [1] to enter the Admin Panel:')
print('Press [2] to enter the Customer Panel:')
print('Press [3] to exit:')
print('\n')


while True:

    option = int(input('Enter Option Number:'))

    if option == 2:

        print('\n\n                               WELCOME TO THE BANK!                               ')
        time.sleep(1.2)

        print('\nWe want to let you know that we have different Banking Operations as described below:')
        time.sleep(1)

        print('1) We have a 12% monthly interest rate which will be added to your account every month.')
        time.sleep(1)

        print('2) We provide loans for the needy person with an interest rate of 15%.\n')
        time.sleep(1.7)

        print('Do you want to create your Account or Login into your Account?')
        print('Press 1 to login into your Account')
        print('Press 2 to create an Account')
        print('Press 3 to exit')

        opt = int(input('Enter Option Number:'))

        if opt == 1:
            person = Customer()
            person.reg_account()

            while True:
                print('What Operation do you want to perform?\n')
                print('Press 1 for Loan')
                print('Press 2 for Monthly Interest')
                print('Press 3 to Withdraw Money')
                print('Press 4 to Deposit Money')
                print('Press 5 to Exit this Section\n')

                ask = int(input('Enter Option Number:\n'))

                if ask == 1:
                    loan = LoanAccount(person.account)
                    loan.user_credit()

                elif ask == 2:
                    interest = SavingAccount(person.account)
                    interest.user_credit()

                elif ask == 3:
                    withdraw = CheckingAccount(person.account, user=person.username)
                    withdraw.user_credit()

                elif ask == 4:
                    depo = CheckingAccount(person.account, user=person.username)
                    depo.deposit_amount()

                elif ask == 5:
                    break
        if opt == 2:
            person = Customer()
            person.create_account()

            while True:
                print('What Operation do you want to perform?')

                print()
                print('Press 1 for Loan')
                print('Press 2 for Monthly Interest')
                print('Press 3 to Withdraw Money')
                print('Press 4 to Exit this Section')
                print()

                ask = int(input('Enter Option Number:'))

                if ask == 1:
                    loan = LoanAccount(person.account)
                    loan.user_credit()

                elif ask == 2:
                    interest = SavingAccount(person.account)
                    interest.user_credit()

                elif ask == 3:
                    withdraw = CheckingAccount(person.account)
                    withdraw.user_credit()

                elif ask == 4:
                    break

        elif opt == 3:
            print('Thank you for visiting!')
            exit()

    elif option == 1:
        print()
        print()
        print("                            WELCOME TO ADMIN SECTION                      ")
        print()
        print("PRESS [0] TO EXIT:\n")
        username = int(input("INPUT ID:"))
        password = int(input("INPUT PASSWORD:"))
        while True:
            if username == 123 and password == 123:
                print()
                print("     ACCESS GRANTED        ")
                print()
                print(f"TO VIEW EACH CUSTOMER FILE PRESS [1]:\nFOR COMPLETE INFO A  PERSON [2]:\nFOR OVERALL "
                      f"TRANSACTION HISTORY PRESS [3]:\nPRESS [0] TO EXIT]:")
                print()

                while True:

                    choice = int(input("ENTER HERE:"))

                    if choice == 1:
                        with open("data.txt", "r") as f:
                            number = 1
                            for line in f:
                                data = line.strip().split(",")
                                print(f'{number})NAME:{data[0]}\n  BALANCE:{data[5]}')
                                number += 1
                                print()

                    elif choice == 2:
                        print()
                        take = input("ENTER NAME OF THE PERSON:")
                        print()
                        print("LOADING...")
                        time.sleep(1)
                        print()
                        with open("data.txt", "r") as f:
                            for lines in f:
                                data = lines.strip().split(",")
                                if data[3] == take:
                                    print(
                                        f'NAME: {data[0]}\nLAST NAME: {data[1]}\nEMAIL ADDRESS: {data[2]}\nUSERNAME: {data[3]}\n'
                                        f'PASSWORD: {data[4]}\nBALANCE:{data[5]}')

                                    with open(take+".txt") as user_hist:
                                        user_trans = user_hist.read()
                                        print("TRANSACTION HISTORY:", user_trans)
                    elif choice == 3:
                        print("OVERALL TRANSACTION HISTORY")
                        print("\nLOADNIG.....\n")

                        with open("GENERALIZED HISTORY.txt","r") as hist:
                            overall_hist=hist.read()
                            print("TRANSACTION HISTORY OF BANK\n\n", overall_hist)

            elif username == 0 or password == 0:
                break

            else:
                print("TRY AGAIN\n")

    else:
        print('INVALID INPUT TRYAGAIN')
        print()


        # def deposit_amount(self):
        #     deposit = abs(int(input('Enter Amount to Deposit Money to the Account:')))
        #     self.balance += deposit
        #     with open('data.txt', 'r+') as file:
        #         data = file.readlines()
        #
        #         for index, line in enumerate(data):
        #             temp_user = line.strip().split(',')
        #             if self.user == temp_user[3]:
        #                 temp_user[5] = str(self.balance)
        #                 data[index] = (",".join(temp_user) + "\n")
        #
        #                 with open(self.user + ".txt", "a") as user_file:
        #                     user_file.write(
        #                         'CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',' + str(
        #                             deposit) + '\n')
        #
        #                 with open('GENERALIZED HISTORY.txt', "a") as hist_file:
        #                     hist_file.write(
        #                         self.user + ' :CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #                         + ',' + str(deposit) + '\n')
        #
        #     with open('data.txt', "w") as f:
        #         for line in data:
        #             f.write(line)