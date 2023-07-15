from datetime import datetime
import time
from abc import ABC, abstractmethod


class Account:
    def __init__(self, balance, user=' '):
        self.balance = balance
        self.user = user

    def deposit(self):
        while True:
            try:
                amount = int(input('Enter amount of Deposit:'))
                self.balance += amount
                print('The Amount is successfully deposited into your Account.\n')
                break
            except ValueError:
                print('Invalid Input!')
                print('Try Again\n')
        with open('data.txt', 'r+') as file:
            data = file.readlines()
            for index, line in enumerate(data):
                temp_user = line.strip().split(',')
                if self.user == temp_user[3]:
                    temp_user[5] = str(self.balance)
                    data[index] = (",".join(temp_user) + "\n")

                    with open(self.user + ".txt", "a") as user_file:
                        user_file.write(
                            'CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',' + str(
                                deposit) + '\n')

                    with open('GENERALIZED HISTORY.txt', "a") as hist_file:
                        hist_file.write(
                            self.user + ' :CASH DEPOSITED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            + ',' + str(deposit) + '\n')

                    print("\nAMOUNT HAS SUCCESSFULLY DEPOSITED INTO YOUR ACCOUNT")
            with open('data.txt', "w") as f:
                for line in data:
                    f.write(line)

    def withdraw(self):
        amount = int(input('Enter amount of withdrawal:'))
        if self.balance >= amount:
            self.balance -= amount
            print('The Amount is successfully withdrawn from your Account.\n')
        else:
            print("Withdrawal isn't possible.")

    def balance_enquiry(self):
        print(f'The current balance in your Account is Rs.{self.balance}\n')


class History(ABC):
    @abstractmethod
    def user_credict(self):
        pass


class CheckingAccount(Account, History):
    def __init__(self, account, credit_limit: int = 3000, user=' '):
        super().__init__(account.balance)
        self.credit_limit = credit_limit
        self.user = user

    def user_credict(self):
        print(f'We provide a credit limit of Rs.{self.credit_limit} with an overdraft fee of Rs.500.\n')
        while True:
            try:
                withdraw = int(input('Enter Amount to Withdraw Money from Account:'))
                break
            except ValueError:
                print('Invalid Input! Try Again')
                print('Please type Integer\n')
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
                            user_file.write(
                                'CASH WITHDRAWAL,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',' + str(
                                    withdraw) + '\n')

                        with open('GENERALIZED HISTORY.txt', "a") as user_file:
                            user_file.write(
                                self.user + ' :CASH WITHDRAWAL,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                + ',' + str(withdraw) + '\n')

            with open('data.txt', "w") as f:
                for line in data:
                    f.write(line)

        elif withdraw > self.balance:
            diff = self.balance - withdraw
            if diff >= -self.credit_limit:
                # over_draft = 500
                print('You do not have sufficient balance, so it will deduct from the credit limit.')
                print('And for this, the overdraft fee is Rs.500')
                self.balance = diff - 500
                with open('data.txt', 'r+') as file:
                    data = file.readlines()
                    for index, line in enumerate(data):
                        temp_user = line.strip().split(',')
                        if self.user == temp_user[3]:
                            temp_user[5] = str(self.balance)
                            data[index] = (",".join(temp_user) + "\n")
                            with open(self.user + ".txt", "a") as user_file:
                                user_file.write('CASH WITHDRAWAL INCLUDING OVERDRAFT FEES,' + datetime.now()
                                                .strftime("%d/%m/%Y %H:%M:%S") + ',' + str(withdraw) + '\n')

                            with open('GENERALIZED HISTORY.txt', "a") as user_file:
                                user_file.write(
                                    self.user + ' :CASH WITHDRAWAL INCLUDING OVERDRAFT FEES,' + datetime.now()
                                    .strftime("%d/%m/%Y %H:%M:%S") + ',' + str(withdraw) + '\n')

                            print(f"CASH WITHDRAWAL OF {withdraw} WSA SUCCESSFUL")

                with open('data.txt', "w") as f:
                    for line in data:
                        f.write(line)
            else:
                print(f'CANNOT EXCEED CREDIT LIMIT OF THE BANK\n')


class SavingAccount(Account, History):
    def __init__(self, account, interest=12):
        super().__init__(account.balance)
        self.interest_rate = interest

    def user_credict(self):
        print(f'\nWe provide a 12% interest rate for our customers.\n')
        interest = (self.interest_rate / 100) * self.balance
        print(f'You have got a monthly interest of Rs.{interest}.')
        self.balance += interest
        time.sleep(1)
        print(f'Monthly Interest is Successfully added into your Account.\n')
        print(f'Your current balance is Rs.{self.balance}.\n')
        time.sleep(1.2)


class LoanAccount(Account, History):
    def __init__(self, account, principal_amount=0, interest=15, loan_dur=0, loan_user=' '):
        super().__init__(account)
        self.principal_amount = principal_amount
        self.interest_rate = interest
        self.loan_duration = loan_dur
        self.loan_user = loan_user

    def user_credict(self):
        print('We got you covered! Our bank provides loans for your needs, but it has some conditions.')
        print('We have an interest rate of 15% for any amount you want.\n')
        while True:
            try:
                self.principal_amount = int(input('Enter amount for the loan:'))
                self.interest_rate = int(15)
                break
            except ValueError:
                print('Invalid Input!')
                print('Try Again\n')
        while True:
            try:
                self.loan_duration = int(input('Enter the duration of the loan in months:'))
                break
            except ValueError:
                print('Invalid Input!')
                print('Try Again\n')

        print(
            f'You demand an amount for the loan Rs.{self.principal_amount} and settle for the duration of {self.loan_duration} months.\n')
        loan = (self.interest_rate / 100) * self.principal_amount * self.loan_duration
        loan = int(loan + self.principal_amount)
        result = int(loan / self.loan_duration)

        print(f'You have to pay the bank Rs.{round(result, 1)} monthly for {self.loan_duration} months.\n')
        time.sleep(1.2)
        with open('loan.txt', "a") as loan_file:
            loan_file.write(f'{self.loan_user},{loan},{self.interest_rate},{self.loan_duration},{result}\n')

        with open(self.loan_user + '.txt', "a") as loan_file:
            loan_file.write('LOAN TAKEN ON ' + str(loan) + 'ON' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')

        with open('GENERALIZED HISTORY.txt', "a") as loan_file:
            loan_file.write(self.loan_user + ':LOAN TAKEN ON ' + str(loan) + 'ON' + datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S") + '\n')


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
            while True:
                self.password = input('Choose a Password for your Bank Account:')
                if len(self.password) <= 6:
                    print('Processing...')
                    time.sleep(1.2)
                    print('Password is too Weak')
                    print('Please choose a Password of 7 letters or more.\n')
                elif len(self.password) >= 7:
                    print('Processing...')
                    time.sleep(1.2)
                    print('Congrats! Your Details are saved.\n')
                    break
            self.account = Account(balance=0)
            self.account.deposit()
            print('Creating your Account! Hold for a while...')
            time.sleep(1)
            print('Loading...')
            time.sleep(1.8)
            print('Your Account is Successfully Registered!')
            self.account.balance_enquiry()
            file.write(
                f'{self.first_Name},{self.last_Name},{self.address},{self.username},{self.password},{self.account.balance}\n')
            time.sleep(1.5)

            with open(self.username + ".txt", "w") as user_file:
                user_file.write('ACCOUNT CREATED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ','
                                + str(self.account.balance) + '\n')

            with open('GENERALIZED HISTORY.txt', "a") as hist_file:
                hist_file.write(
                    self.username + ' :ACCOUNT CREATED,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "," +
                    str(self.account.balance) + '\n')

    def reg_account(self):
        while True:
            self.username = input('Enter your Username:')
            self.password = input('Enter your Password:')
            with open('data.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if self.username == data[3] and self.password == data[4]:
                        with open(self.username + ".txt", "a") as user_file:
                            user_file.write(
                                'SIGNED IN,' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ',None' + '\n')

                        with open('GENERALIZED HISTORY.txt', "a") as user_file:
                            user_file.write(self.username + ' :SIGNED IN,' + datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S") + ',None' + '\n')
                        print('Searching your Account! Wait...')
                        time.sleep(1)
                        print('Loading...')
                        time.sleep(1.8)
                        print('\nAccount Verified!')
                        time.sleep(1)
                        print()
                        print(f'Welcome Back {data[0]} {data[1]}\n')
                        self.account = Account(int(data[5]))
                        print(f'You have a current balance of {data[5]}\n')
                        time.sleep(1.5)
                        return

            print('Searching your Account! Wait...')
            time.sleep(1)
            print('Loading...')
            time.sleep(1.8)
            print('Invalid username or password. Please try again.\n')


while True:
    print('Press [1] to enter the Admin Panel')
    print('Press [2] to enter the Customer Panel')
    print('Press [3] to exit\n')
    option = int(input('Enter Option Number:'))
    if option == 2:
        print('\n\n\n                               WELCOME  TO  THE  BANK!                               ')
        time.sleep(1.2)
        print('\nWe want to let you know that we have different Banking Operations as described below:')
        time.sleep(1)
        print('1) We have a 12% monthly interest rate which will be added to your account every month.')
        time.sleep(1)
        print('2) We provide loans for the needy person with an interest rate of 15%.\n')
        time.sleep(1.5)
        print('Do you want to create your Account or Login into your Account?')
        print('Press [1] to login into your Account')
        print('Press [2] to create an Account')
        print('Press [3] to exit')
        opt = int(input('Enter Option Number:'))
        if opt == 1:
            person = Customer()
            person.reg_account()
            while True:
                print('What Operation do you want to perform?\n')
                time.sleep(1)
                print('Press [1] for Loan:')
                time.sleep(0.7)
                print('Press [2] for Monthly Interest:')
                time.sleep(0.7)
                print('Press [3] to Withdraw Money:')
                time.sleep(0.7)
                print('Press [4] to Deposit Money:')
                time.sleep(0.7)
                print('Press [5] to View Transaction:')
                time.sleep(0.7)
                print('Press [6] to Exit this Section\n')
                time.sleep(0.7)
                ask = int(input('Enter Option Number:\n'))
                if ask == 1:
                    loan = LoanAccount(person.account, loan_user=person.username)

                    with open('loan.txt', 'r') as f:
                        usernames = set(line.strip().split(',')[0] for line in f)

                    if person.username in usernames:
                        print("YOU HAVE ALREADY TAKEN THE LOAN\n ")
                        print("PRESS [0] TO EXIT\n")
                        loan_input = input("WANT TO PAY IT?\n[Y]for YES [N] for NO: \n").upper()

                        while True:
                            if loan_input == "Y":
                                with open("loan.txt", "r") as file:
                                    data = file.readlines()

                                for index, line in enumerate(data):
                                    temp_user = line.strip().split(',')
                                    if person.username == temp_user[0]:
                                        print("PRESS [0] TO EXIT\n")

                                        print(
                                            f'Hey {person.username}\n\nHOW YOU WANT TO PAY\n 1) {temp_user[4]} MONTHLY'
                                            f'\n 2)  {temp_user[1]} ALL\n')

                                        loan_in = int(input("ENTER CHOICE:"))
                                        while True:
                                            if loan_in == 1:

                                                temp_user[1] = str(int(temp_user[1]) - int(temp_user[4]))
                                                temp_user[3] = str(int(temp_user[3]) - 1)
                                                data[index] = (",".join(temp_user) + "\n")

                                                if temp_user[1] == "0":
                                                    del data[index]
                                                    print("LOAN CLEARED\n")
                                                    with open(person.username + ".txt", "a") as user_file:
                                                        user_file.write(
                                                            'LOAN CLEARED ON,' + datetime.now()
                                                            .strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                    with open('GENERALIZED HISTORY.txt', "a") as user_file:
                                                        user_file.write(
                                                            person.username + ' :LOAN CLEARED ON,' +
                                                            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                else:
                                                    pass
                                                    print(f"\nONE MONTH LOAN HAS BEEN PAYED NOW HAVE TO PAY SAME "
                                                          f"AMOUNT FOR {int(temp_user[3])} MONTHS\n")

                                                    with open(person.username + ".txt", "a") as user_file:
                                                        user_file.write(
                                                            'LOAN FOR ONE MONTH CLEARED,' + datetime.now()
                                                            .strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                    with open('GENERALIZED HISTORY.txt', "a") as user_file:
                                                        user_file.write(
                                                            person.username + ' :LOAN FOR ONE MONTH CLEARED ON,' +
                                                            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                break
                                            elif loan_in == 2:

                                                temp_user[1], temp_user[4], temp_user[3] = str(0), str(0), str(0)
                                                data[index] = (",".join(temp_user) + "\n")

                                                print(f'LOAN HAS BEEN CLEARED')

                                                with open(person.username + ".txt", "a") as user_file:
                                                    user_file.write('LOAN CLEARED,' +
                                                                    datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                with open('GENERALIZED HISTORY.txt', "a") as user_file:
                                                    user_file.write(person.username + ' :LOAN CLEARED,' +
                                                                    datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')

                                                del data[index]
                                                break

                                            elif loan_in == 0:
                                                break

                                            else:
                                                print("TRY AGAIN\n")

                                        break

                                with open('loan.txt', "w") as f:
                                    for line in data:
                                        f.write(line)

                                break

                            elif loan_input == "N":
                                print("SORRY YOU CANT NOT TAKE FURTHER LOAN")
                                break

                            elif loan_input == "0":
                                break

                            else:
                                print("INVALID INPUT\nTRYAGAIN\n")

                    else:
                        loan.user_credict()

                elif ask == 2:
                    interest = SavingAccount(person.account)
                    interest.user_credict()

                elif ask == 3:
                    withdraw = CheckingAccount(person.account, user=person.username)
                    if person.account.balance < 0:
                        print("YOU ARE ALREADY IN DEBT CANT WITHDRAW\n")
                    else:
                        withdraw.user_credict()

                elif ask == 4:
                    with open("data.txt", "r") as f:
                        data = f.readlines()
                        for lines in data:
                            data = lines.strip().split(",")
                            if data[3] == person.username:
                                current_balance = data[5]
                    depo = Account(int(current_balance), user=person.username)
                    depo.deposit()
                elif ask == 5:
                    print("\nLOADING....\n")
                    time.sleep(1)
                    with open(person.username + ".txt") as user_hist:
                        user_trans = user_hist.read()
                        print("TRANSACTION HISTORY:", user_trans)
                elif ask == 6:
                    print('Logging out...')
                    time.sleep(1.5)
                    print('You are Log out successfully.\n')
                    print('Thank you for choosing our Bank!')
                    break
                else:
                    print('Error! Invalid Choice.')
                    print('Please choose from the given options.\n')
                    time.sleep(1)
                    continue
        if opt == 2:
            person = Customer()
            person.create_account()
            while True:
                print('What Operation do you want to perform?\n')
                time.sleep(1)
                print('Press 1 for Loan')
                time.sleep(0.7)
                print('Press 2 for Monthly Interest')
                time.sleep(0.7)
                print('Press 3 to Withdraw Money')
                time.sleep(0.7)
                print('Press 4 to Exit this Section')
                time.sleep(0.7)
                ask = int(input('Enter Option Number:'))
                if ask == 1:
                    loan = LoanAccount(person.account, loan_user=person.username)
                    loan.user_credict()
                elif ask == 2:
                    interest = SavingAccount(person.account)
                    interest.user_credict()
                elif ask == 3:
                    withdraw = CheckingAccount(person.account, user=person.username)
                    withdraw.user_credict()
                elif ask == 4:
                    print('Logging out...')
                    time.sleep(1.5)
                    print('You are Log out successfully.\n')
                    print('Thank you for choosing our Bank!')
                    break
                else:
                    print('Error! Invalid Choice.')
                    print('Please choose from the given options.\n')
                    time.sleep(1)
                    continue

        elif opt == 3:
            print('Thank you for visiting!')
            exit()

    elif option == 1:
        print()
        print()
        print("                            WELCOME  TO  ADMIN  SECTION                      ")
        print()
        print("PRESS [0] TO EXIT:\n")

        while True:
            username = int(input("INPUT ID:"))
            password = int(input("INPUT PASSWORD:"))
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

                                    with open(take + ".txt") as user_hist:
                                        user_trans = user_hist.read()
                                        print("TRANSACTION HISTORY:", user_trans)
                    elif choice == 3:
                        print("OVERALL TRANSACTION HISTORY")
                        print("\nLOADNIG.....\n")

                        with open("GENERALIZED HISTORY.txt", "r") as hist:
                            overall_hist = hist.read()
                            print("TRANSACTION HISTORY OF BANK\n\n", overall_hist)
            elif username == 0 or password == 0:
                print('Program Ended!')
                break

            else:
                print("TRY AGAIN\n")

    else:
        print('INVALID INPUT TRYAGAIN')
