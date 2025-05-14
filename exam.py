import os
from datetime import datetime
from colorama import Fore,Back,Style,init
init(autoreset=True)
#"pip install colorama" run in command prompt

#==============================================================***ID GENERATOR***===================================================================================================#

def create_customer_next_id():
    if not os.path.exists("customer.txt") or os.path.getsize("customer.txt") == 0:
        return "C0001"
    with open("customer.txt", "r") as customer_file:
        return f"C{int(customer_file.readlines()[-1].split(',')[0][1:]) + 1:04}"

def create_user_next_id():
    if not os.path.exists("user.txt") or os.path.getsize("user.txt") == 0:
        return "U0001"
    with open("user.txt", "r") as user_file:
        return f"U{int(user_file.readlines()[-1].split(',')[0][1:]) + 1:04}"

#====================================================================***ADMIN***==================================================================================================#

def create_first_admin():
    if not os.path.exists("user.txt") or os.path.getsize("user.txt") == 0:
        admin_name = "ADMIN"
        admin_password = "Sathu15"
        with open("user.txt", "a") as user_file:
            user_file.write(f"{create_user_next_id()},{admin_name},{admin_password},Admin\n")
        print(f"Admin Login Details: Username: {admin_name}, Password: {admin_password}")

#===================================================================***VALID INPUT***================================================================================================#

def get_valid_input(prompt):
        while True:
            value = input(prompt).strip()
            if value:  
                return value
            else:
                print("Input cannot be empty. Please enter a valid value.")

#==========EXAM 01=======================================#

def Display_customer_list():
    with open ("customer.txt", "r") as customer_file:
        count = 0
        for line in customer_file:
            count =+ 1
            parts = line.strip().split(",")
            print(parts[0], ":", parts[1])
Display_customer_list()

#===============Exam 2====================================#

def Total_Users():
    count = 0  
    with open ("user.txt", "r") as user_file:
        for line in user_file:
            line = user_file.readlines()
            count += 1
            total = line

        print("Total Users: ", total)
Total_Users()


#=================================================================***CUSTOMER INFOMATION***===========================================================================================#

def get_customer_info():
    while True:
        username = get_valid_input("Enter customer's username: ") 
        with open("user.txt", "r") as file:
            for line in file:
                
                parts = line.strip().split(",")
                parts[1] = username
                if not username in line :
                    print("successfully!!!")
                    
                else:
                    print("Username already taken. Try another!")
                    continue
                    
        password = get_valid_input("Enter customer's password: ")
        name = get_valid_input("Enter customer's name: ")
        NIC = get_valid_input("Enter customer's NIC NO: ")
        age = get_valid_input("Enter customer's age: ")
        gender = get_valid_input("Female or Male: ")
        address = get_valid_input("Enter customer's address: ")
        phone = get_valid_input("Enter customer's phone number: ")
        return{
                "username": username,
                "password": password,
                "name": name,
                "NIC_NO": NIC,
                "age": age,
                "gender": gender,
                "address": address,
                "Phone_No": phone
            }           
                            
get_customer_info()

            
    
    
   

#=================================================================***CREATE CUSTOMER AND USER***===================================================================================#

def create_customer_and_user():
    customer = get_customer_info()
    with open("customer.txt", "a") as customer_file, open("user.txt", "a") as user_file:
        customer_id = create_customer_next_id()
        user_id = create_user_next_id()
        customer_file.write(f"{customer_id},{customer['name']},{customer['NIC_NO']},{customer['age']},{customer['gender']},{customer['address']},{customer['Phone_No']}\n")
        user_file.write(f"{user_id},{customer['username']},{customer['password']},Customer\n")
        print(f"Customer and user created successfully. Customer ID: {customer_id}, User ID: {user_id}")

#===================================================================***CREATE ACCOUNT***=============================================================================================#

def create_new_account():
    id_number = input("Enter customer ID number: ")

    found = False
    try:
        with open("customer.txt", "r") as customer_file:
            for line in customer_file:
                if line.startswith(id_number):
                    found = True
                    break
    except FileNotFoundError:
        print("Customer file not found.")
        return

    if not found:
        print("Customer ID not found. Please create customer first.")
        return

    account_num = 1000000
    try:
        with open("accounts.txt", "r") as account_file:
            lines = account_file.readlines()
        count = len(lines)
    except FileNotFoundError:
        count = 0

    new_account_no = account_num + count
    try:
        ac_balance = float(input("Enter your deposit money: "))
        if ac_balance < 1000:
            print("Minimum deposit should be at least 1000.")
            return

        with open("accounts.txt", "a") as account_file:
            account_file.write(f"{id_number},{new_account_no},{ac_balance}\n")

        print(f"New account created successfully! Account Number: {new_account_no}, Balance: {ac_balance}")

        time_menu = datetime.now().strftime("%d-%m-%Y %A %I:%M %p")
        with open("transaction.txt", "a") as file:
            file.write(f"{account_num},initial_amount,{ac_balance},{ac_balance},{time_menu}\n")
    except ValueError:
        print("Invalid input for balance.")

#=====================================================================***BALANCE***==================================================================================================#

def check_balance():
    acc_no = input("Enter your account number: ").strip()
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[1] == acc_no:
                    print(f"Account Number: {acc_no}, Balance: {parts[2]}")
                    return
        print("Account not found.")
    except FileNotFoundError:
        print("Account file not found.")

#=======================================================================***TRANSACTIONS***===========================================================================================#

def amount_input():
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                raise ValueError("Amount must be grater than 0.")
            return amount
        except ValueError:
            print("Invalid input. Try again!!!.")

#==========================================================================***DEPOSIT***=============================================================================================#

def deposit():
    account_number = input("Enter account number: ").strip()
    updated = False
    try:
        with open("accounts.txt", "r") as file:
            lines = file.readlines()

        with open("accounts.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(",")
                if parts[1] == account_number:
                    balance = float(parts[2])
                    deposit_amount = amount_input()
                    new_balance = balance + deposit_amount
                    file.write(f"{parts[0]},{account_number},{new_balance}\n")
                    updated = True

                    time_menu = datetime.now().strftime("%d-%m-%Y %A %I:%M %p")
                    with open("transaction.txt", "a") as trans_file:
                        trans_file.write(f"{account_number},deposit,{deposit_amount},{new_balance},{time_menu}\n")
                    print(f"Deposit successful! New balance: {new_balance}")
                else:
                    file.write(line)

        if not updated:
            print("Account not found.")
    except FileNotFoundError:
        print("accounts.txt not found.")

#========================================================================***WITHDRAW***==============================================================================================#
def withdraw():
    acc_no = input("Enter account number: ").strip()
    updated = False
    try:
        with open("accounts.txt", "r") as file:
            lines = file.readlines()

        with open("accounts.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(",")
                if parts[1] == acc_no:
                    balance = float(parts[2])
                    withdraw_amt = amount_input()
                    if withdraw_amt <= balance:
                        new_balance = balance - withdraw_amt
                        file.write(f"{parts[0]},{acc_no},{new_balance}\n")
                        updated = True

                        timestamp = datetime.now().strftime("%d-%m-%Y %A %I:%M %p")
                        with open("transaction.txt", "a") as trans_file:
                            trans_file.write(f"{acc_no},Withdraw,{withdraw_amt},{new_balance},{timestamp}\n")
                        print(f"Withdraw successful! New balance: {new_balance}")
                    else:
                        print("Insufficient balance.")
                        file.write(line)
                else:
                    file.write(line)

        if not updated:
            print("Account not found.")
    except FileNotFoundError:
        print("account_no.txt not found.")

#======================================================================***UPDATE***===============================================================================================#

def update_customer():
    customer_id = input("Enter customer ID: ")
    updated = False

    try:
        with open("customer.txt", "r") as file:
            lines = file.readlines()

        with open("customer.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(",")
                if parts[0] == customer_id:
                    updated = True
                    print("1. Name\n2. NIC\n3. Age\n4. Gender\n5. Address\n6. Phone")
                    choice = input("Enter field to update: ")

                    if choice == "1":
                        parts[1] = get_valid_input("New name: ")
                    elif choice == "2":
                        parts[2] = get_valid_input("New NIC: ")
                    elif choice == "3":
                        parts[3] = get_valid_input("New age: ")
                    elif choice == "4":
                        parts[4] = get_valid_input("New gender: ")
                    elif choice == "5":
                        parts[5] = get_valid_input("New address: ")
                    elif choice == "6":
                        parts[6] = get_valid_input("New phone: ")

                    file.write(",".join(parts) + "\n")
                else:
                    file.write(line)

        if updated:
            print("Customer updated successfully.")
        else:
            print("Customer ID not found.")

    except FileNotFoundError:
        print("customer.txt not found.")

#=============================================================***TRANSFER MONEY***=================================================================================================#
def transfer_money():
    print("\n************* TRANSFER MONEY *************")

    from_acc = input("Enter Your Account Number: ").strip()
    to_acc = input("Enter Recipient's Account Number: ").strip()
    amount = amount_input()

    accounts = {}
    updated = False

    try:

        with open("accounts.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    accounts[parts[1]] = [parts[0], float(parts[2])]

        if from_acc  == to_acc:
            print("You cannot transfer to the same account.")
            return
        if from_acc not in accounts:
            print("Sender account not found.")
            return
        if to_acc not in accounts:
            print("Recipient account not found.")
            return

        if accounts[from_acc][1] < amount:
            print("Insufficient balance.")
            return


        accounts[from_acc][1] -= amount
        accounts[to_acc][1] += amount
        updated = True

        with open("accounts.txt", "w") as file:
            for acc_num, data in accounts.items():
                file.write(f"{data[0]},{acc_num},{data[1]:.2f}\n")


        time_menu = datetime.now().strftime("%d-%m-%Y %A %I:%M %p")
        with open("transaction.txt", "a") as trans_file:
            trans_file.write(f"{from_acc},transfer,{amount},{accounts[from_acc][1]},{time_menu}\n")
            trans_file.write(f"{to_acc},received,{amount},{accounts[to_acc][1]},{time_menu}\n")
        print(f"Transfer successful! New balance of sender ({from_acc}): {accounts[from_acc][1]:.2f}")

    except FileNotFoundError:
        print("accounts.txt not found.")

#================================================================***TRANSACTION HISTORY***=========================================================================================#

def transaction_history():
    account_no = input("Enter Your Account Number: ").strip()
    found = False
    try:
        with open("transaction.txt", "r") as transaction_file:
            print(f"{'account_number' :<35}{'current_balance':<20}{'deposit/withdrawal' :<25}{'amount' :<15}{'time'}\n")
            for line in transaction_file:
                transaction_data = line.strip().split(',')
                if account_no == transaction_data[0]:
                    print(f"{transaction_data[0]:<35}{transaction_data[1]:<20}{transaction_data[2]:<25}{transaction_data[3]:<15}{transaction_data[4]}\n")
                    found = True
            if not found:
                print("No transaction history found!!!")
    except FileNotFoundError:
        print("Transaction file not found!!!")
#=====================================================================***ADMIN & CUSTOMER MENU***==================================================================================#

def admin_menu():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    found = False
    try:
        with open("user.txt", "r") as user_file:
            for line in user_file:
                parts = line.strip().split(",")
                if len(parts) >= 4 and parts[1] == username and parts[2] == password:
                    print("Login successful!")
                
       
                    while True:
                        print("\nAdmin Menu")
                        print("1. Create User")
                        print("2. Create Account")
                        print("3. Deposit")
                        print("4. Withdraw")
                        print("5. Transfer Money")
                        print("6. View Transaction history")
                        print("7. Check Balance")
                        print("8. Update Customer")
                        print("9. Exit")

                        choice = input("Enter choice: ")

                        if choice == "1":
                            create_customer_and_user()
                        elif choice == "2":
                            create_new_account()
                        elif choice == "3":
                            deposit()
                        elif choice == "4":
                            withdraw()
                        elif choice == "5":
                            transfer_money()
                        elif choice == "6":
                            transaction_history()
                        elif choice == "7":
                            check_balance()
                        elif choice == "8":
                            update_customer()
                        elif choice == "9":
                            break
                        else:
                            print("Invalid input.")
                        found = True
                        break
            if not found:
                print("Invalid UserName or Pasword!")
    
    except FileNotFoundError:
        print("User file not found.")

#================================================================================***CUSTOMER MENU***============================================================================#                  

def customer_menu():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    found = False
    try:
        with open("user.txt", "r") as user_file:
            for line in user_file:
                parts = line.strip().split(",")
                if len(parts) >= 4 and parts[1] == username and parts[2] == password:
                    print("Login successful!")
                    while True:
                        print("\nCustomer Menu")
                        print("1. Deposit")
                        print("2. Withdraw")
                        print("3. Transfer Money")
                        print("4. View Transaction history")
                        print("5. Check Balance")
                        print("6. Exit")

                        choice = input("Enter choice: ")

                        if choice == "1":
                            deposit()
                        elif choice == "2":
                            withdraw()
                        elif choice == "3":
                            transfer_money()
                        elif choice == "4":
                            transaction_history()
                        elif choice == "5":
                            check_balance()
                        elif choice == "6":
                            break
                        else:
                            print("Invalid input.")

                        found = True
                        break
            if not found:
                print("Invalid UserName or Pasword!")
    
    except FileNotFoundError:
        print("User file not found.")

#=============================================================***ADMIN OR CUSTOMER OPTION***==========================================================================================#

def select_option_ad_or_cus():
    while True:

        print(Fore.CYAN+"!!!Select the Role Admin or Customer!!! ")
        print("Enter Number '1' if you are Admin: ")
        print("Enter Number '2' if you are Customer: ")
        print("Enter Number '3' if you want Exit: ")

        select_option = input("Enter a Number '1' or '2' or '3': ")

        if select_option == '1':
             admin_menu()
        elif select_option == '2':
            customer_menu()
        elif select_option == '3':
            print("!!!THANK YOU!!!")
            exit()
        
        else:
            print("!!!...Enter Number Only '1' OR '2'...!!!")

#==========================================================================***MAIN***===============================================================================================#

# def main():
#     create_first_admin()
#     select_option_ad_or_cus()
    
# if __name__ == "__main__":
#     main()

#************=================================================************************************=====================================================================************#
