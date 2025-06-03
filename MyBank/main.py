import sqlite3
from db import initialize_db
from auth import register, login
from bank import deposit, withdraw, check_balance, transaction_history, transfer, account_details
from termcolor import colored

def main():
    initialize_db()
    user_id = None

    while True:
        if not user_id:
            print(colored("\n1. Register\n2. Login\n3. Exit", "light_cyan"))
            choice = input("Select option: ")
            if choice == "1":
                user_id = register()
            elif choice == "2":
                user_id = login()
            elif choice == "3":
                print(colored("Goodbye!", "green"))
                break
            else:
                print(colored("Invalid option.", "red"))
        else:
            print(colored("\n =======Welcome to my Banking app=======\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transaction History\n5. Transfer\n6. Account Details\n7. Logout", "light_blue"))
            choice = input("Select option: ")
            if choice == "1":
                deposit(user_id)
            elif choice == "2":
                withdraw(user_id)
            elif choice == "3":
                check_balance(user_id)
            elif choice == "4":
                transaction_history(user_id)
            elif choice == "5":
                transfer(user_id)
            elif choice == "6":
                account_details(user_id)
            elif choice == "7":
                user_id = None
                print(colored("Logged out.", "light_yellow"))
            else:
                print(colored("Invalid option.", "red"))

if __name__ == "__main__":
    main()
    

# try:
#     main()
# except sqlite3.IntegrityError as e:
#     print(e)
# except sqlite3.OperationalError as e:
#     print(e)
# except Exception as e:
#     print(f"Something went wrong: {e}")
# finally:
#     conn.close()