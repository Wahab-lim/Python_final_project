import re
import random
import getpass
import hashlib
from db import get_connection

from termcolor import colored

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    return (
        8 <= len(password) <= 30 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def generate_account_number():
    conn = get_connection()
    c = conn.cursor()
    while True:
        acc_num = str(random.randint(10**7, 10**8 - 1))
        c.execute("SELECT 1 FROM users WHERE account_number = ?", (acc_num,))
        if not c.fetchone():
            return acc_num

def register():
    full_name = input("Full Name: ").strip()
    if not full_name or not re.fullmatch(r"[A-Za-z ]{4,255}", full_name):
        print(colored("Invalid full name.", "red"))
        return

    username = input("Username: ").strip()
    if not re.fullmatch(r"\w{3,20}", username):
        print(colored("Invalid username.", "red"))
        return

    while True:
        password = getpass.getpass("Password: ")
        if validate_password(password):
            break
        print(colored("Password must be 8-30 chars with uppercase, lowercase, number, and symbol.", "red"))

    try:
        deposit = float(input("Initial Deposit (min 2000): "))
        if deposit < 2000:
            print(colored("Minimum deposit is 2000.", "red"))
            return
    except ValueError:
        print(colored("Invalid deposit amount.", "red"))
        return
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if c.fetchone():
        print(colored("Username already exists.", "red"))
        return

    _ = colored("Registration successful", "green")
    acc_num = generate_account_number()
    password_hash = hash_password(password)
    c.execute("INSERT INTO users (full_name, username, password_hash, account_number, balance) VALUES (?, ?, ?, ?, ?)",
              (full_name, username, password_hash, acc_num, deposit))
    conn.commit()
    print(f"{_}. Your account number is {acc_num}.")
    return login()

def login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    if not password.strip():
        print(colored("Password cannot be blank.","red"))
        return None

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result and hash_password(password) == result[1]:
        print(colored("Login successful.", "green"))
        return result[0]
    else:
        print(colored("Invalid username or password.", "red"))
        return None
