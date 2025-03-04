# auth.py
import pandas as pd
import os
import hashlib

USER_CSV = './docs/user.csv'
ORDER_CSV = './docs/orders.csv'  # New CSV for orders

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user
def register_user(username, email, password):
    if not os.path.exists(USER_CSV):
        df = pd.DataFrame(columns=['username', 'email', 'password'])
        df.to_csv(USER_CSV, index=False)

    df = pd.read_csv(USER_CSV)
    if username in df['username'].values:
        return "Username already exists."
    if email in df['email'].values:
        return "Email already exists."

    hashed_password = hash_password(password)
    new_user = pd.DataFrame({'username': [username], 'email': [email], 'password': [hashed_password]})
    new_user.to_csv(USER_CSV, mode='a', header=False, index=False)
    return "User  registered successfully."

# Function to login a user using email and password
def login_user(email, password):
    if not os.path.exists(USER_CSV):
        return "User  not found.", None, None

    df = pd.read_csv(USER_CSV)
    if email not in df['email'].values:
        return "User  not found.", None, None

    hashed_password = hash_password(password)
    user_data = df[df['email'] == email]
    if user_data['password'].values[0] == hashed_password:
        return "Login successful.", user_data['username'].values[0], user_data['email'].values[0]
    else:
        return "Invalid password.", None, None

# Function to add an order
def add_order(username, product_name, quantity):
    if not os.path.exists(ORDER_CSV):
        df = pd.DataFrame(columns=['username', 'product_name', 'quantity'])
        df.to_csv(ORDER_CSV, index=False)

    new_order = pd.DataFrame({'username': [username], 'product_name': [product_name], 'quantity': [quantity]})
    new_order.to_csv(ORDER_CSV, mode='a', header=False, index=False)
    return "Order added successfully."

# Function to list orders for a user
def list_orders(username):
    if not os.path.exists(ORDER_CSV):
        return pd.DataFrame(columns=['username', 'product_name', 'quantity'])

    df = pd.read_csv(ORDER_CSV)
    user_orders = df[df['username'] == username]
    return user_orders

# Function to delete an order
def delete_order(username, product_name):
    if not os.path.exists(ORDER_CSV):
        return "No orders found."

    df = pd.read_csv(ORDER_CSV)
    df = df[~((df['username'] == username) & (df['product_name'] == product_name))]
    df.to_csv(ORDER_CSV, index=False)
    return "Order deleted successfully."
