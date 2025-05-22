# Bank Management System

A console-based Python application implementing a simple bank management system with three user roles (Admin, Staff, Customer).  
Customers can hold up to two accounts (“normal” and “fixed”), deposit/withdraw only from their normal account, and view balances & transaction history.  
Admin and Staff can manage users and customer accounts.

---

## Table of Contents

1. Features  
2. Folder Structure  
3. Prerequisites  
4. Setup & Run  
5. Usage  
6. Data Files  
7. How It Works  
8. Error Handling  
9. License

---

## Features

- **Role-Based Login**: Admin / Staff / Customer  
- **Admin & Staff**  
  - View / Add / Delete Staff  
  - Create Customer (inline username & password)  
  - Create / Delete / Update Customer Bank Accounts  
  - View all accounts & transactions  
- **Customer**  
  - Holds up to 2 accounts (one **normal**, one **fixed**)  
  - Deposit / Withdraw (only on **normal** account)  
  - View My Accounts  
  - View My Transactions  
- **Auto-Generated Account IDs**  
- **File Persistence** via `users.txt`, `accounts.txt`, `transactions.txt`  
- **Graceful Input Validation** and **“exit”** shortcuts

---

## Folder Structure

```
/project-root
│
├── bank_management_system_.py   # Main Python script
├── users.txt                    # “username,password,role” records
├── accounts.txt                 # “account_id,username,type,balance” records
├── transactions.txt             # “account_id,txn_type,amount,timestamp,username” records
└── README.md                    # This file
```

---

## Prerequisites

- Python **3.7+** installed  
- (Optional) A terminal or console—no GUI dependencies  

---

## Setup & Run

1. **Clone** or **unzip** the project folder.  
2. Ensure the three data files exist (empty or pre-populated):  
   ```bash
   touch users.txt accounts.txt transactions.txt
   ```  
3. **Run** the script:
   ```bash
   python bank_management_system_.py
   ```

---

## Usage

1. **Main Menu**  
   ```
   1. Login
   2. Exit
   ```
2. **Login**  
   - Enter your **username**, **password**, and **role** (admin/staff/customer).  
   - Role prompt loops until correct.  

3. **Admin Menu**  
   - View / Add / Delete Staff  
   - Create Customer Account  
   - Delete / Update Account  
   - View All Accounts / Transactions  
   - Logout  

4. **Staff Menu**  
   - Create Customer Account  
   - View / Delete / Update Accounts  
   - View All Transactions  
   - Logout  

5. **Customer Menu**  
   - Deposit (normal account only)  
   - Withdraw (normal account only)  
   - View My Accounts  
   - View My Transactions  
   - Logout  

> Typing **`exit`** at any sub-prompt returns you to the previous menu.

---

## Data Files

### `users.txt`

Each line:  
```
<username>,<password>,<role>
```
- **role** ∈ {`admin`, `staff`, `customer`}

### `accounts.txt`

Each line:  
```
<account_id>,<username>,<type>,<balance>
```
- **type** ∈ {`normal`, `fixed`}

### `transactions.txt`

Each line:  
```
<account_id>,<txn_type>,<amount>,<timestamp>,<username>
```
- **txn_type** ∈ {`deposit`, `withdraw`}

---

## How It Works

- On **Login**, credentials are checked against `users.txt`.  
- **Admin/Staff** can inline-create a new customer:  
  1. Prompt for username & password → adds to `users.txt` if new  
  2. Prompt for account type & balance → writes to `accounts.txt` with auto-ID  
- **Customer** operations append to `transactions.txt` and update `accounts.txt` balances.  
- All file I/O uses `with open(...)` blocks.

---

## Error Handling

- Invalid numeric/menu selections are re-prompted.  
- Empty or numeric-only usernames are rejected.  
- Attempting to deposit/withdraw on a “fixed” account is blocked.  
- Insufficient balance aborts the transaction with an error.  
- Missing data files are auto-created empty on startup.

---

## License

This code is provided as-is for the **ABC** assignment.  
