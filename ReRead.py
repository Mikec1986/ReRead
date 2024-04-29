import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from user import *
from book import *
from inventory import *
from PIL import Image, ImageTk


# Global variable to track login status
global logged_in
logged_in = False

class MainPage:
    """
    Class representing the main page of the application.
    """

    def __init__(self, master, db_connection, inventory_db_connection):
        """
        Initialize the main page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
        """
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Main Page")
        self.master.configure(background='#D0E7F9')  # Soft blue background color

        self.load_and_display_image()
        
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
        """
        Log out the user.
        """
        global logged_in
        logged_in = False
        self.master.destroy()
        main()


    def open_inventory_window(self):
        """
        Open the inventory window.
        """
        self.master.withdraw()  # Hide the main window
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("ReRead - Inventory")
        inventory_window.configure(bg='#D0E7F9')
        inventory_window.protocol("WM_DELETE_WINDOW", self.on_inventory_window_close)
        InventoryPage(inventory_window, self.db_connection, self.inventory_db_connection)

    def open_cart_window(self):
        """
        Open the cart window.
        """
        self.master.withdraw()  # Hide the main window
        cart_window = tk.Toplevel(self.master)
        cart_window.protocol("WM_DELETE_WINDOW", self.on_cart_window_close)
        cart_window.title("ReRead - View Cart")
        cart_window.configure(bg='#D0E7F9')
        CartPage(cart_window)

    def open_login_window(self):
        """
        Open the login window.
        """
        self.master.withdraw()  # Hide the main window
        login_window = tk.Toplevel(self.master)
        login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)
        login_window.title("ReRead - Login")
        login_window.configure(bg='#D0E7F9')
        LoginPage(login_window, self.db_connection, self.inventory_db_connection)
        
    def load_and_display_image(self):
        """
        Load and display the image on the main window.
        """
        # Load the image
        image_path = "books.jpg"  # Adjust the path accordingly
        image = Image.open(image_path)

        # Resize the image if needed
        image = image.resize((400, 200))  # Adjust width and height as needed

        # Convert the image to a format compatible with Tkinter
        photo = ImageTk.PhotoImage(image)

        # Create a Label widget to display the image
        image_label = tk.Label(self.master, image=photo, bg='#D0E7F9')
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.pack()

    def open_register_window(self):
        """
        Open the registration window.
        """
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_window_close)
        register_window.title("ReRead - Registration")
        register_window.configure(bg='#D0E7F9')
        RegistrationPage(register_window, self.db_connection)

    # Show the main window when window is closed
    def on_inventory_window_close(self):
        """
        Callback when the inventory window is closed.
        """
        self.master.destroy()
        main()

    def on_cart_window_close(self):
        """
        Callback when the cart window is closed.
        """
        self.master.destroy()
        main()

    def on_register_window_close(self):
        """
        Callback when the register window is closed.
        """
        self.master.destroy()
        main()

    def on_login_window_close(self):
        """
        Callback when the login window is closed.
        """
        self.master.destroy()
        main()

class SellPage:
    """
    Class representing the page for selling a book.
    """

    def __init__(self, master, inventory_db_connection):
        """
        Initialize the sell page.

        Args:
            master (tk.Tk): The master Tkinter window.
            inventory_db_connection: SQLite database connection for inventory data.
        """
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
        """
        Sell a book.
        """
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
    """
    Class representing the inventory page.
    """

    def __init__(self, master, db_connection, inventory_db_connection):
        """
        Initialize the inventory page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
        """
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

        sell_button = tk.Button(master, text="Sell", command=self.open_sell_page, font=("Arial", 12),
                                bg='green', fg='white')
        sell_button.pack(pady=10)


    def populate_inventory(self):
        """
        Populate the inventory list.
        """
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("SELECT * FROM inventory")
        books = cursor.fetchall()

        for book in books:
            self.inventory_tree.insert("", "end", text=book[0], values=(book[1], book[2], book[5], book[6]))

    def open_sell_page(self):
        """
        Open the sell page.
        """
        sell_window = tk.Toplevel(self.master)
        sell_window.title("ReRead - Sell Book")
        sell_window.configure(bg='#D0E7F9')
        SellPage(sell_window, self.db_connection)

class CartPage:
    """
    Class representing the cart page.
    """

    def __init__(self, master):
        """
        Initialize the cart page.

        Args:
            master (tk.Tk): The master Tkinter window.
        """
        self.master = master
        self.master.configure(bg='#D0E7F9')

        # Implement cart functionality here


class RegistrationPage:
    """
    Class representing the registration page.
    """

    def __init__(self, master, db_connection):
        """
        Initialize the registration page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
        """
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

        tk.Label(master, text="Email:", font=("Arial", 12), bg='#D0E7F9').pack()  # Changed "Password" to "Email"
        self.email_entry = tk.Entry(master, font=("Arial", 12))
        self.email_entry.pack()  # Changed show="*" to normal entry for email

        # Register Button
        register_button = tk.Button(master, text="Register", command=self.register_user, font=("Arial", 12),
                                    bg='green', fg='white')
        register_button.pack(pady=10)

    def register_user(self):
        """
        Register a new user.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()  # Added email retrieval

        if not username or not password or not email:  # Check for email as well
            messagebox.showerror("Error", "Please enter both username, password, and email.")  # Updated error message
            return

        # Check if username already exists
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))  # Updated query
        self.db_connection.commit()

        # Get the last inserted row ID (auto-incremented)
        user_id = cursor.lastrowid

        # Format the user ID to a four-digit number
        user_id_four_digits = '{:04d}'.format(user_id)

        print("User ID (Four digits):", user_id_four_digits)

        messagebox.showinfo("Success", "Registration successful!")
        global logged_in  # Added global keyword to modify the global variable
        logged_in = True

        # Clear entry fields after registration
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)  # Clear email entry field

class LoginPage:
    """
    Class representing the login page.
    """

    def __init__(self, master, db_connection, inventory_db_connection):
        """
        Initialize the login page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
        """
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Login")
        self.master.configure(background='#D0E7F9')  # Soft blue background color
        
         # Load and display the login image
        login_image = Image.open("login.png")  
        resized_login_image = login_image.resize((200, 200))
        login_photo = ImageTk.PhotoImage(resized_login_image)

        login_label = tk.Label(master, image=login_photo, bg='#D0E7F9')
        login_label.image = login_photo
        login_label.pack()

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
        """
        Log in the user.
        """
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
    global logged_in
    db_connection = sqlite3.connect("user_database.db")
    cursor = db_connection.cursor()

    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        email TEXT)''')  # Added email column

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
