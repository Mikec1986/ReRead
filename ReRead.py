import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from user import *
from book import *
from inventory import *

global logged_in
logged_in = False

class MainPage:
    def __init__(self, master, db_connection, inventory_db_connection):
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection  # Store inventory_db_connection
        self.master.title("ReRead - Main Page")
        self.master.configure(background='#D0E7F9')  # Soft blue background color

        # Introduction
        intro_text = """
        Welcome to ReRead - where the love for books meets the joy of recycling! 
        Dive into our virtual bookstore, where every page holds a story and every purchase breathes new life into pre-loved books.
        Search for your next literary adventure, add favorites to your cart, and embark on a journey through the endless shelves of knowledge.
        Let's rediscover the magic of reading while also caring for our planet. Happy browsing!
        """
        intro_label = tk.Label(master, text=intro_text, wraplength=400, justify="center", font=("Arial", 12),
                               bg='#D0E7F9')  # Set background color
        intro_label.pack()

        inventory_button = tk.Button(master, text="Inventory", command=self.open_inventory_window, font=("Arial", 12),
                                  bg='blue', fg='white')  # Set button color
        inventory_button.pack(pady=5)

        view_cart_button = tk.Button(master, text="View Cart", command=self.open_cart_window, font=("Arial", 12),
                                     bg='blue', fg='white')
        view_cart_button.pack(pady=5)

        if not logged_in:
            # Login and Register buttons
            login_button = tk.Button(master, text="Login", command=self.open_login_window, font=("Arial", 12),
                                     bg='green', fg='white')
            login_button.pack(pady=5)

            register_button = tk.Button(master, text="Register", command=self.open_register_window, font=("Arial", 12),
                                        bg='green', fg='white')
            register_button.pack(pady=5)

        if logged_in:
            logout_button = tk.Button(master, text="Log Out", command=self.logout, font=("Arial", 12),
                                     bg='green', fg='white')
            logout_button.pack(pady=5)

    def logout(self):
        global logged_in
        logged_in = False
        self.master.destroy()
        main()


    def open_inventory_window(self):
        self.master.withdraw()  # Hide the main window
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("ReRead - Inventory")
        inventory_window.configure(bg='#D0E7F9')
        inventory_window.protocol("WM_DELETE_WINDOW", self.on_inventory_window_close)
        InventoryPage(inventory_window, self.db_connection, self.inventory_db_connection)

    def open_cart_window(self):
        self.master.withdraw()  # Hide the main window
        cart_window = tk.Toplevel(self.master)
        cart_window.protocol("WM_DELETE_WINDOW", self.on_cart_window_close)
        cart_window.title("ReRead - View Cart")
        cart_window.configure(bg='#D0E7F9')
        CartPage(cart_window)

    def open_login_window(self):
        self.master.withdraw()  # Hide the main window
        login_window = tk.Toplevel(self.master)
        login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)
        login_window.title("ReRead - Login")
        login_window.configure(bg='#D0E7F9')
        LoginPage(login_window, self.db_connection, self.inventory_db_connection)

    def open_register_window(self):
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_window_close)
        register_window.title("ReRead - Registration")
        register_window.configure(bg='#D0E7F9')
        RegistrationPage(register_window, self.db_connection)

    # Show the main window when window is closed
    def on_inventory_window_close(self):
        self.master.destroy()
        main()

    def on_cart_window_close(self):
        self.master.destroy()
        main()

    def on_register_window_close(self):
        self.master.destroy()
        main()

    def on_login_window_close(self):
        self.master.destroy()
        main()

class SellPage:
    def __init__(self, master, inventory_db_connection):
        self.master = master
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Sell Book")
        self.master.configure(background='#D0E7F9')

        # Labels and Entry Widgets for the book details form
        tk.Label(master, text="Title:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.title_entry = tk.Entry(master, font=("Arial", 12))
        self.title_entry.pack()

        tk.Label(master, text="Author:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.author_entry = tk.Entry(master, font=("Arial", 12))
        self.author_entry.pack()

        tk.Label(master, text="Price:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.price_entry = tk.Entry(master, font=("Arial", 12))
        self.price_entry.pack()

        tk.Label(master, text="Quantity:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.quantity_entry = tk.Entry(master, font=("Arial", 12))
        self.quantity_entry.pack()

        sell_button = tk.Button(master, text="Sell", command=self.sell_book, font=("Arial", 12),
                                bg='green', fg='white')
        sell_button.pack(pady=10)

    def sell_book(self):
        # Get book details from the form
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        # Validate input
        if not title or not author or not price or not quantity:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert book into the inventory database
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("INSERT INTO inventory (title, author, price, quantity) VALUES (?, ?, ?, ?)",
                       (title, author, price, quantity))
        self.inventory_db_connection.commit()

        messagebox.showinfo("Success", "Book added to inventory successfully!")
        self.master.destroy()


class InventoryPage:
    def __init__(self, master, db_connection, inventory_db_connection):
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.master.configure(bg='#D0E7F9')

        self.inventory_tree = ttk.Treeview(master)
        self.inventory_tree["columns"] = ("Title", "Author", "Price", "Quantity")
        self.inventory_tree.heading("#0", text="ID")
        self.inventory_tree.column("#0", width=50)
        self.inventory_tree.heading("Title", text="Title")
        self.inventory_tree.heading("Author", text="Author")
        self.inventory_tree.heading("Price", text="Price")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.pack(padx=10, pady=10)
        self.populate_inventory()

        #search_button = tk.Button(master, text="Search", command=self.search_books, font=("Arial", 12),
        #                          bg='blue', fg='white')
        #search_button.pack(pady=10)

        sell_button = tk.Button(master, text="Sell", command=self.open_sell_page, font=("Arial", 12),
                                bg='green', fg='white')
        sell_button.pack(pady=10)


    def populate_inventory(self):
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("SELECT * FROM inventory")
        books = cursor.fetchall()
        print(books)

        for book in books:
            self.inventory_tree.insert("", "end", text=book[0], values=(book[1], book[2], book[5], book[6]))

    def open_sell_page(self):
        sell_window = tk.Toplevel(self.master)
        sell_window.title("ReRead - Sell Book")
        sell_window.configure(bg='#D0E7F9')
        SellPage(sell_window, self.db_connection)

class CartPage:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='#D0E7F9')

        # Implement cart functionality here


class RegistrationPage:
    def __init__(self, master, db_connection):
        self.master = master
        self.db_connection = db_connection
        self.master.title("ReRead - Registration")
        self.master.configure(background='#D0E7F9')  # Soft blue background color

        # Labels and Entry Widgets
        tk.Label(master, text="Username:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.username_entry = tk.Entry(master, font=("Arial", 12))
        self.username_entry.pack()

        tk.Label(master, text="Password:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.password_entry = tk.Entry(master, show="*", font=("Arial", 12))
        self.password_entry.pack()

        tk.Label(master, text="Password:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.email_entry = tk.Entry(master, show="*", font=("Arial", 12))
        self.email_entry.pack()

        # Register Button
        register_button = tk.Button(master, text="Register", command=self.register_user, font=("Arial", 12),
                                    bg='green', fg='white')
        register_button.pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            tk.messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check if username already exists
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            tk.messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.db_connection.commit()

        # Get the last inserted row ID (auto-incremented)
        user_id = cursor.lastrowid

        # Format the user ID to a four-digit number
        user_id_four_digits = '{:04d}'.format(user_id)

        print("User ID (Four digits):", user_id_four_digits)

        tk.messagebox.showinfo("Success", "Registration successful!")
        logged_in = True

        # Clear entry fields after registration
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

class LoginPage:
    def __init__(self, master, db_connection, inventory_db_connection):
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Login")
        self.master.configure(background='#D0E7F9')  # Soft blue background color

        # Labels and Entry Widgets
        tk.Label(master, text="Username:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.username_entry = tk.Entry(master, font=("Arial", 12))
        self.username_entry.pack()

        tk.Label(master, text="Password:", font=("Arial", 12), bg='#D0E7F9').pack()
        self.password_entry = tk.Entry(master, show="*", font=("Arial", 12))
        self.password_entry.pack()

        # Login Button
        login_button = tk.Button(master, text="Login", command=self.login_user, font=("Arial", 12),
                                 bg='green', fg='white')
        login_button.pack(pady=10)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        global logged_in

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check if username and password match
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            logged_in = True
            self.master.withdraw()  # Hide the login window


            self.master.destroy()
            main()

        else:
            messagebox.showerror("Error", "Invalid username or password.")


def main():
    # Create a SQLite database connection
    print(logged_in)
    db_connection = sqlite3.connect("user_database.db")
    cursor = db_connection.cursor()

    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    inventory_db_connection = sqlite3.connect("inventory_database.db")
    cursor_inventory = inventory_db_connection.cursor()

    # Create inventory table if not exists
    cursor_inventory.execute('''CREATE TABLE IF NOT EXISTS inventory (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 title TEXT,
                                 author TEXT,
                                 ISBN TEXT,
                                 condition TEXT,
                                 price REAL,
                                 quantity INTEGER)''')

    root = tk.Tk()
    main_page = MainPage(root, db_connection, inventory_db_connection)

    def on_closing():
        # Close database connections
        db_connection.close()
        inventory_db_connection.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()



if __name__ == "__main__":
    main()
