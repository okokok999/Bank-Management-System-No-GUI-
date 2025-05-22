# -*- coding: utf-8 -*-
"""Bank Management System"""

import os
from datetime import datetime

# --- Helper Functions ---

def ensure_file(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()

def get_valid_int(prompt, min_val=1, max_val=None, allow_exit=False):
    while True:
        val = input(prompt).strip()
        if allow_exit and val.lower() == 'exit':
            return None
        try:
            num = int(val)
            if num < min_val or (max_val is not None and num > max_val):
                print("\033[91m❌ Invalid selection.\033[0m")
            else:
                return num
        except ValueError:
            print("\033[91m❌ Invalid input. Please enter a number.\033[0m")

def get_customer_accounts(username):
    """Return list of [id, user, type, balance] for this customer, without printing."""
    ensure_file("accounts.txt")
    result = []
    with open("accounts.txt", 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 4 and parts[1] == username:
                result.append(parts)
    return result

# --- User Class ---

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = None

    def validate_credentials(self):
        ensure_file("users.txt")
        with open("users.txt", 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 3:
                    continue
                u, p, r = parts
                if self.username == u and self.password == p:
                    self.role = r
                    return True
        print("\033[91m❌ Login failed: Invalid credentials.\033[0m")
        return False

    def validate_role(self, input_role):
        return self.role == input_role

# --- Admin / Staff Functions ---

def list_staff():
    ensure_file("users.txt")
    staff = []
    with open("users.txt", 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[2].lower() == 'staff':
                staff.append(parts)
    print("\n--- Staff List ---")
    for i, s in enumerate(staff, 1):
        print(f"{i}. Username: {s[0]}")
    return staff

def add_staff():
    print("\n--- Add New Staff ---")
    username = input("Enter new staff username (or 'exit'): ").strip()
    if username.lower() == 'exit':
        return
    if username.isdigit():
        print("\033[91m❌ Username cannot be numeric.\033[0m")
        return
    password = input("Enter password: ").strip()
    if not username or not password:
        print("\033[91m❌ Username and password cannot be empty.\033[0m")
        return
    ensure_file("users.txt")
    with open("users.txt", 'r') as f:
        if any(line.startswith(username + ",") for line in f):
            print("\033[91m❌ Username already exists.\033[0m")
            return
    with open("users.txt", 'a') as f:
        f.write(f"{username},{password},staff\n")
    print("\033[92m✅ Staff added.\033[0m")

def delete_staff():
    staff = list_staff()
    if not staff:
        print("\033[91m❌ No staff to delete.\033[0m")
        return
    choice = get_valid_int("Select staff to delete by number (or 'exit'): ",
                           1, len(staff), allow_exit=True)
    if choice is None:
        return
    target = staff[choice - 1][0]
    with open("users.txt", 'r') as f:
        lines = f.readlines()
    with open("users.txt", 'w') as f:
        for line in lines:
            if not (line.startswith(target + ",") and line.strip().endswith(",staff")):
                f.write(line)
    print("\033[92m✅ Staff deleted.\033[0m")

# --- Account Management ---

def list_accounts(filter_user=None):
    ensure_file("accounts.txt")
    accounts = []
    with open("accounts.txt", 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 4:
                accounts.append(parts)
    if filter_user:
        accounts = [acc for acc in accounts if acc[1] == filter_user]
    print("\n--- Account List ---")
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. ID: {acc[0]} | User: {acc[1]} | Type: {acc[2]} | Balance: ${acc[3]}")
    return accounts

def create_account():
    print("\n--- Create New Account ---")
    ensure_file("users.txt")
    ensure_file("accounts.txt")
    # Auto-generate next Account ID
    ids = []
    with open("accounts.txt", 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts and parts[0].isdigit():
                ids.append(int(parts[0]))
    new_id = str(max(ids, default=1000) + 1)

    # Customer username & password inline
    username = input("Enter customer username (or 'exit'): ").strip()
    if username.lower() == 'exit':
        return
    if username.isdigit():
        print("\033[91m❌ Username cannot be numeric.\033[0m")
        return
    password = input("Enter customer password: ").strip()
    if not password:
        print("\033[91m❌ Password cannot be empty.\033[0m")
        return

    # Add to users.txt if not existing
    ensure_file("users.txt")
    with open("users.txt", 'r') as f:
        exists = any(line.startswith(username + ",") for line in f)
    if not exists:
        with open("users.txt", 'a') as f:
            f.write(f"{username},{password},customer\n")

    # Enforce max 2 accounts per customer
    existing = get_customer_accounts(username)
    if len(existing) >= 2:
        print("\033[91m❌ Customer already has 2 accounts.\033[0m")
        return

    # Choose account type
    types = ["normal", "fixed"]
    print("Account types:")
    for idx, t in enumerate(types, 1):
        print(f" {idx}. {t}")
    t_choice = get_valid_int("Select type number (or 'exit'): ",
                             1, len(types), allow_exit=True)
    if t_choice is None:
        return
    acctype = types[t_choice - 1]
    if any(acc[2] == acctype for acc in existing):
        print("\033[91m❌ Customer already has this account type.\033[0m")
        return

    # Initial balance
    balance = input("Initial balance: ").strip()
    if not balance.replace('.', '', 1).isdigit():
        print("\033[91m❌ Balance must be a number.\033[0m")
        return

    # Write account record
    with open("accounts.txt", 'a') as f:
        f.write(f"{new_id},{username},{acctype},{balance}\n")
    print(f"\033[92m✅ Account created. (ID {new_id})\033[0m")

def delete_account():
    accounts = list_accounts()
    if not accounts:
        print("\033[91m❌ No accounts to delete.\033[0m")
        return
    choice = get_valid_int("Select account to delete by number (or 'exit'): ",
                           1, len(accounts), allow_exit=True)
    if choice is None:
        return
    target = accounts[choice - 1][0]
    with open("accounts.txt", 'r') as f:
        lines = f.readlines()
    with open("accounts.txt", 'w') as f:
        for line in lines:
            if not line.startswith(target + ","):
                f.write(line)
    print("\033[92m✅ Account deleted.\033[0m")

def update_account():
    accounts = list_accounts()
    if not accounts:
        print("\033[91m❌ No accounts to update.\033[0m")
        return
    choice = get_valid_int("Select account to update by number (or 'exit'): ",
                           1, len(accounts), allow_exit=True)
    if choice is None:
        return
    target = accounts[choice - 1]
    new_balance = input("Enter new balance (or 'exit'): ").strip()
    if new_balance.lower() == 'exit':
        return
    if not new_balance.replace('.', '', 1).isdigit():
        print("\033[91m❌ Balance must be a number.\033[0m")
        return
    with open("accounts.txt", 'r') as f:
        lines = f.readlines()
    with open("accounts.txt", 'w') as f:
        for line in lines:
            if line.startswith(target[0] + ","):
                f.write(f"{target[0]},{target[1]},{target[2]},{new_balance}\n")
            else:
                f.write(line)
    print("\033[92m✅ Account updated.\033[0m")

# --- Customer Functions ---

def select_account(username):
    accounts = list_accounts(filter_user=username)
    if not accounts:
        print("\033[91m❌ No accounts found.\033[0m")
        return None
    choice = get_valid_int("Select account by number (or 'exit'): ",
                           1, len(accounts), allow_exit=True)
    return accounts[choice - 1][0] if choice else None

def perform_transaction(acc_id, username, amount, t_type):
    with open("accounts.txt", 'r') as f:
        lines = f.readlines()
    updated = False
    with open("accounts.txt", 'w') as f:
        for line in lines:
            aid, user, acctype, bal = line.strip().split(',')
            if aid == acc_id and user == username:
                new_bal = float(bal) + amount
                if new_bal < 0:
                    print("\033[91m❌ Insufficient funds.\033[0m")
                    f.write(line)
                    return
                f.write(f"{aid},{user},{acctype},{new_bal:.2f}\n")
                ensure_file("transactions.txt")
                with open("transactions.txt", 'a') as tf:
                    tf.write(f"{aid},{t_type},{abs(amount):.2f},"
                             f"{datetime.now()},{user}\n")
                updated = True
            else:
                f.write(line)
    if updated:
        print("\033[92m✅ Transaction successful.\033[0m")

def view_transactions(username=None):
    ensure_file("transactions.txt")
    with open("transactions.txt", 'r') as f:
        lines = f.readlines()
    if not lines:
        print("No transactions recorded.")
        return
    print("\n--- Transaction History ---")
    found = False
    for line in lines:
        parts = line.strip().split(',', 4)
        if len(parts) < 5:
            continue
        aid, t_type, amt, dt, user = parts
        if username is None or username == user:
            print(f"{dt} | Account: {aid} | {t_type.title()} | ${amt}")
            found = True
    if username and not found:
        print("No transactions found for this user.")

# --- Menus ---

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Staff")
        print("2. Add Staff")
        print("3. Delete Staff")
        print("4. Create Customer Account")
        print("5. Delete Account")
        print("6. Update Account")
        print("7. View All Accounts")
        print("8. View All Transactions")
        print("9. Logout")
        ch = input("Choose: ").strip()
        if ch == '1': list_staff()
        elif ch == '2': add_staff()
        elif ch == '3': delete_staff()
        elif ch == '4': create_account()
        elif ch == '5': delete_account()
        elif ch == '6': update_account()
        elif ch == '7': list_accounts()
        elif ch == '8': view_transactions()
        elif ch == '9': break
        else: print("\033[91m❌ Invalid input.\033[0m")

def staff_menu():
    while True:
        print("\n--- Staff Menu ---")
        print("1. Create Customer Account")
        print("2. View Accounts")
        print("3. Delete Account")
        print("4. Update Account")
        print("5. View All Transactions")
        print("6. Logout")
        ch = input("Choose: ").strip()
        if ch == '1': create_account()
        elif ch == '2': list_accounts()
        elif ch == '3': delete_account()
        elif ch == '4': update_account()
        elif ch == '5': view_transactions()
        elif ch == '6': break
        else: print("\033[91m❌ Invalid input.\033[0m")

def customer_menu(username):
    def get_account_type(acc_id):
        with open("accounts.txt", 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == acc_id:
                    return parts[2]
        return None

    while True:
        print(f"\n--- Customer Menu ({username}) ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View My Accounts")
        print("4. View My Transactions")
        print("5. Logout")
        ch = input("Choose: ").strip()
        if ch == '1':
            acc_id = select_account(username)
            if acc_id:
                if get_account_type(acc_id) == 'fixed':
                    print("\033[91m❌ Cannot deposit into a fixed account.\033[0m")
                    continue
                amt = input("Enter deposit amount (or 'exit'): ").strip()
                if amt.lower() != 'exit':
                    if not amt.replace('.', '', 1).isdigit():
                        print("\033[91m❌ Invalid amount.\033[0m")
                    else:
                        perform_transaction(acc_id, username,
                                            float(amt), "deposit")
        elif ch == '2':
            acc_id = select_account(username)
            if acc_id:
                if get_account_type(acc_id) == 'fixed':
                    print("\033[91m❌ Cannot withdraw from a fixed account.\033[0m")
                    continue
                amt = input("Enter withdrawal amount (or 'exit'): ").strip()
                if amt.lower() != 'exit':
                    if not amt.replace('.', '', 1).isdigit():
                        print("\033[91m❌ Invalid amount.\033[0m")
                    else:
                        perform_transaction(acc_id, username,
                                            -float(amt), "withdraw")
        elif ch == '3':
            list_accounts(filter_user=username)
        elif ch == '4':
            view_transactions(username)
        elif ch == '5':
            break
        else:
            print("\033[91m❌ Invalid input.\033[0m")

# --- Login System & Main ---

def login():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = User(username, password)
    if user.validate_credentials():
        # Loop until correct role entered
        while True:
            role = input("Role (admin/staff/customer): ").lower().strip()
            if user.validate_role(role):
                break
            print("\033[91m❌ Incorrect role. Please enter a valid role.\033[0m")
        print(f"\033[92m✅ Logged in as {role}: {username}\033[0m")
        if role == 'admin':
            admin_menu()
        elif role == 'staff':
            staff_menu()
        elif role == 'customer':
            customer_menu(username)

def main():
    while True:
        print("\n=== Bank Management System ===")
        print("1. Login")
        print("2. Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            login()
        elif choice == '2':
            break
        else:
            print("\033[91m❌ Invalid input.\033[0m")

if __name__ == '__main__':
    main()
