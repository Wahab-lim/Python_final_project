import time
from db import get_connection

from termcolor import colored

def deposit(user_id):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print(colored("Invalid amount.", "red"))
        return
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    c.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'Deposit', ?)", (user_id, amount))
    conn.commit()
    time.sleep(2)
    print(colored("Deposit successful.","green"))

def withdraw(user_id):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print(colored("Invalid amount.", "red"))
        return
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = c.fetchone()[0]

    if amount > balance:
        print(colored("Insufficient balance.", "red"))
        return

    c.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
    c.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'Withdrawal', ?)", (user_id, amount))
    conn.commit()
    time.sleep(2)
    print(colored("Withdrawal successful.", "green"))

def check_balance(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = c.fetchone()[0]
    current_balance = colored("Current balance", "blue")
    print(f"{current_balance}: ₦{balance:.2f}")

def transaction_history(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT type, amount, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    transactions = c.fetchall()
    if not transactions:
        print(colored("No transactions found.", "yellow"))
    else:
        print(colored("\nTransaction History:", "cyan"))
        for t in transactions:
            print(f"{t[2]} - {t[0]}: ₦{t[1]:.2f}")

def transfer(user_id):
    recipient = input("Enter recipient account number: ").strip()
    if not recipient.isdigit():
        print(colored("Invalid account number.", "red"))
        return

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT account_number FROM users WHERE id = ?", (user_id,))
    self_acc = c.fetchone()[0]
    if recipient == self_acc:
        print(colored("Cannot transfer to your own account.", "red"))
        return

    c.execute("SELECT id FROM users WHERE account_number = ?", (recipient,))
    recipient_data = c.fetchone()
    if not recipient_data:
        print(colored("Recipient not found.", "red"))
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print(colored("Invalid amount.", "red"))
        return
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

    c.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = c.fetchone()[0]
    if amount > balance:
        print(colored("Insufficient funds.", "red"))
        return

    c.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
    c.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, recipient_data[0]))
    c.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'Transfer Out', ?)", (user_id, amount))
    c.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, 'Transfer In', ?)", (recipient_data[0], amount))
    conn.commit()
    time.sleep(2)
    print(colored("Transfer successful.", "green"))

def account_details(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT full_name, username, account_number FROM users WHERE id = ?", (user_id,))
    details = c.fetchone()
    print(f"Full Name: {details[0]}\nUsername: {details[1]}\nAccount Number: {details[2]}")

