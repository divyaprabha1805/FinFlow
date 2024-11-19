import tkinter as tk
from tkinter import messagebox
import os

USER_FILE = 'users.txt'
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Load users from file
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            for line in file:
                username, pin, balance = line.strip().split(',')
                users[username] = {'pin': pin, 'balance': int(balance)}
    return users

# Save users to file
def save_users():
    with open(USER_FILE, 'w') as file:
        for username, details in users.items():
            file.write(f"{username},{details['pin']},{details['balance']}\n")

# Center a window on the screen
def center_window(window):
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
    y = (window.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
    window.geometry(f"+{x}+{y}")

# Add User Functionality
def add_user():
    def save_new_user():
        username = username_entry.get().lower()
        pin = pin_entry.get()
        balance = balance_entry.get()

        # Validate input
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        elif not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits.")
        elif not balance.isdigit() or int(balance) < 0:
            messagebox.showerror("Error", "Balance must be a valid positive number.")
        else:
            # Add new user to the users dictionary
            users[username] = {'pin': pin, 'balance': int(balance)}
            save_users()  # Save to file
            messagebox.showinfo("Success", f"User {username.capitalize()} added successfully!")
            add_user_window.destroy()

    # Create new window for adding user
    add_user_window = tk.Toplevel()
    add_user_window.title("Add New User")
    center_window(add_user_window)
    add_user_window.configure(bg="#f1f8e9")

    tk.Label(add_user_window, text="Enter username:", bg="#f1f8e9", font=("Arial", 14)).pack(pady=10)
    username_entry = tk.Entry(add_user_window, font=("Arial", 14))
    username_entry.pack(pady=10)

    tk.Label(add_user_window, text="Enter PIN (4 digits):", bg="#f1f8e9", font=("Arial", 14)).pack(pady=10)
    pin_entry = tk.Entry(add_user_window, show="*", font=("Arial", 14))
    pin_entry.pack(pady=10)

    tk.Label(add_user_window, text="Enter initial balance:", bg="#f1f8e9", font=("Arial", 14)).pack(pady=10)
    balance_entry = tk.Entry(add_user_window, font=("Arial", 14))
    balance_entry.pack(pady=10)

    tk.Button(add_user_window, text="Add User", command=save_new_user, bg="#388e3c", fg="white", font=("Arial", 14)).pack(pady=20)

# Login function
def login():
    username = username_entry.get().lower()
    pin = pin_entry.get()
    if username in users and users[username]['pin'] == pin:
        messagebox.showinfo("Login Success", f"Welcome, {username.capitalize()}!")
        main_menu(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or PIN.")

# Main menu
def main_menu(username):
    login_window.destroy()
    menu_window = tk.Tk()
    menu_window.title("Banking System")
    menu_window.configure(bg="#c8e6c9")
    center_window(menu_window)

    tk.Label(menu_window, text=f"Welcome, {username.capitalize()}!", bg="#c8e6c9", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(menu_window, text="Check Balance", command=lambda: messagebox.showinfo("Balance", f"Your balance is {users[username]['balance']} rupees."),
              bg="#388e3c", fg="white", font=("Arial", 14), width=20).pack(pady=10)
    tk.Button(menu_window, text="Deposit Money", command=lambda: deposit(username),
              bg="#00796b", fg="white", font=("Arial", 14), width=20).pack(pady=10)
    tk.Button(menu_window, text="Withdraw Money", command=lambda: withdraw(username),
              bg="#e65100", fg="white", font=("Arial", 14), width=20).pack(pady=10)
    tk.Button(menu_window, text="Change PIN", command=lambda: change_pin(username),
              bg="#4527a0", fg="white", font=("Arial", 14), width=20).pack(pady=10)
    tk.Button(menu_window, text="Logout", command=lambda: [menu_window.destroy(), main()],
              bg="#d32f2f", fg="white", font=("Arial", 14), width=20).pack(pady=20)

    menu_window.mainloop()

# Main login screen
def main():
    global users, login_window, username_entry, pin_entry
    users = load_users()

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="#bbdefb")
    center_window(login_window)

    tk.Label(login_window, text="Welcome to the Banking System", bg="#bbdefb", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(login_window, text="Username:", bg="#bbdefb", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.pack(pady=10)

    tk.Label(login_window, text="PIN:", bg="#bbdefb", font=("Arial", 12)).pack(pady=5)
    pin_entry = tk.Entry(login_window, show="*", font=("Arial", 14))
    pin_entry.pack(pady=10)

    tk.Button(login_window, text="Login", command=login, bg="#0d47a1", fg="white", font=("Arial", 14)).pack(pady=20)
    tk.Button(login_window, text="Add User", command=add_user, bg="#0288d1", fg="white", font=("Arial", 14)).pack(pady=10)  # Add User Button

    login_window.mainloop()

if __name__ == "__main__":
    main()
