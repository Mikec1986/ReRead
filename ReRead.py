# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

# Global variables
global logged_in
logged_in = False
global userID
userID = None

# Main Page Class
class MainPage:
    def __init__(self, master, db_connection, inventory_db_connection, cart=None):
        """
        Initialize the main page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
            cart (list): Optional parameter representing the cart.
        """
        # Initialize attributes
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.cart = cart if cart is not None else []  # Initialize cart as an empty list if not provided

        # Configure master window
        self.master.title("ReRead - Main Page")
        self.master.configure(background='#F7F7F7')
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load and display image
        image_path = "books.jpg"
        image = Image.open(image_path).resize((600, 400))
        self.photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.master, image=self.photo, bg='#F7F7F7')
        image_label.image = self.photo
        image_label.pack()

        # Introduction text
        intro_text = """
        Welcome to ReRead - where the love for books meets the joy of recycling! 
        Dive into our virtual bookstore, where every page holds a story and every purchase breathes new life into pre-loved books.
        Search for your next literary adventure, add favorites to your cart, and embark on a journey through the endless shelves of knowledge.
        Let's rediscover the magic of reading while also caring for our planet. Happy browsing!
        """
        intro_label = tk.Label(master, text=intro_text, wraplength=400, justify="center", font=("Arial", 12),
                               bg='#F7F7F7')
        intro_label.pack()

        # Inventory button
        inventory_button = tk.Button(master, text="Inventory", command=self.open_inventory_window, font=("Arial", 12),
                                     bg='#007BFF', fg='white')
        inventory_button.pack(pady=5)

        # Conditionally display login and register buttons
        if not logged_in:
            login_button = tk.Button(master, text="Login", command=self.open_login_window, font=("Arial", 12),
                                     bg='#28A745', fg='white')
            login_button.pack(pady=5)

            register_button = tk.Button(master, text="Register", command=self.open_register_window, font=("Arial", 12),
                                        bg='#28A745', fg='white')
            register_button.pack(pady=5)
        else:
            view_cart_button = tk.Button(master, text="View Cart", command=self.open_cart_window, font=("Arial", 12),
                                         bg='#007BFF', fg='white')
            view_cart_button.pack(pady=5)

            logout_button = tk.Button(master, text="Log Out", command=self.logout, font=("Arial", 12),
                                      bg='#DC3545', fg='white')
            logout_button.pack(pady=5)

    # Method to logout user
    def logout(self):
        global logged_in
        logged_in = False
        self.master.destroy()
        main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)

    # Method to clear cart
    def clear_cart(self):
        """
        Clears the cart after checkout.
        """
        self.cart = []

    # Method to open inventory window
    def open_inventory_window(self):
        """
        Open the inventory window.
        """
        self.master.withdraw()  # Hide the main window
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("ReRead - Inventory")
        inventory_window.configure(bg='#F7F7F7')
        inventory_window.protocol("WM_DELETE_WINDOW", self.on_inventory_window_close)
        InventoryPage(inventory_window, self.db_connection, self.inventory_db_connection, self.cart, self.open_cart_window)

    # Method to open cart window
    def open_cart_window(self):
        """
        Open the cart window.
        """
        self.master.withdraw()  # Hide the main window
        cart_window = tk.Toplevel(self.master)
        cart_window.protocol("WM_DELETE_WINDOW", self.on_cart_window_close)
        cart_window.title("ReRead - View Cart")
        cart_window.configure(bg='#F7F7F7')
        CartPage(cart_window, self.cart, self.db_connection, self.inventory_db_connection, self.clear_cart)

    # Method to open login window
    def open_login_window(self):
        """
        Open the login window.
        """
        self.master.withdraw()  # Hide the main window
        login_window = tk.Toplevel(self.master)
        login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)
        login_window.title("ReRead - Login")
        login_window.configure(bg='#F7F7F7')
        LoginPage(login_window, self.db_connection, self.inventory_db_connection)

    # Method to open register window
    def open_register_window(self):
        """
        Open the registration window.
        """
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_window_close)
        register_window.title("ReRead - Registration")
        register_window.configure(bg='#F7F7F7')
        RegistrationPage(register_window, self.db_connection)

    # Method to handle inventory window close event
    def on_inventory_window_close(self):
        """
        Callback when the inventory window is closed.
        """
        self.master.destroy()
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection, self.cart)
        else:
            main()

    # Method to handle cart window close event
    def on_cart_window_close(self):
        """
        Callback when the cart window is closed.
        """
        self.master.destroy()
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
        else:
            main()

    # Method to handle register window close event
    def on_register_window_close(self):
        """
        Callback when the register window is closed.
        """
        self.master.destroy()
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
        else:
            main()

    # Method to handle login window close event
    def on_login_window_close(self):
        """
        Callback when the login window is closed.
        """
        self.master.destroy()
        self.photo = None
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
        else:
            main()

    # Method to handle main window close event
    def on_closing(self):
        """
        Callback when the main window is closed.
        """
        # Close database connections
        self.db_connection.close()
        self.inventory_db_connection.close()
        global logged_in
        logged_in = False
        self.master.quit()
        self.master.destroy()

# Sell Page Class
class SellPage:
    def __init__(self, master, inventory_db_connection):
        """
        Initialize the sell page.

        Args:
            master (tk.Tk): The master Tkinter window.
            inventory_db_connection: SQLite database connection for inventory data.
        """
        # Initialize attributes
        self.master = master
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Sell Book")
        self.master.configure(background='#F7F7F7')

        # Labels and Entry Widgets for the book details form
        tk.Label(master, text="Title:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.title_entry = tk.Entry(master, font=("Arial", 12))
        self.title_entry.pack()

        tk.Label(master, text="Author:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.author_entry = tk.Entry(master, font=("Arial", 12))
        self.author_entry.pack()

        tk.Label(master, text="Price:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.price_entry = tk.Entry(master, font=("Arial", 12))
        self.price_entry.pack()

        tk.Label(master, text="Quantity:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.quantity_entry = tk.Entry(master, font=("Arial", 12))
        self.quantity_entry.pack()

        # Sell button
        sell_button = tk.Button(master, text="Sell", command=self.sell_book, font=("Arial", 12),
                                bg='#007BFF', fg='white')
        sell_button.pack(pady=10)

    # Method to sell book
    def sell_book(self):
        """
        Sell a book. Insert book into inventory database
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

# Inventory Page Class
class InventoryPage:
    def __init__(self, master, db_connection, inventory_db_connection, cart, open_cart_window):
        """
        Initialize the inventory page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
            cart (list): The cart.
            open_cart_window (function): Function to open cart window.
        """
        # Initialize attributes
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.cart = cart
        self.open_cart_window2 = open_cart_window
        self.master.configure(bg='#F7F7F7')

        # Inventory Treeview
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

        # Refresh button
        refresh_button = tk.Button(master, text="Refresh", command=self.refresh_inventory, font=("Arial", 12),
                                   bg='blue', fg='white')
        refresh_button.pack(pady=10)

        # Conditionally display sell and cart buttons
        if logged_in:
            sell_button = tk.Button(master, text="Sell", command=self.open_sell_page, font=("Arial", 12),
                                    bg='#007BFF', fg='white')
            sell_button.pack(pady=10)

            add_to_cart_button = tk.Button(master, text="Add to Cart", command=self.add_to_cart, font=("Arial", 12),
                                           bg='#007BFF', fg='white')
            add_to_cart_button.pack(pady=10)

            view_cart_button = tk.Button(master, text="View Cart", command=self.open_cart_window2, font=("Arial", 12),
                                         bg='#007BFF', fg='white')
            view_cart_button.pack(pady=5)
        else:
            tk.Label(master, text="Return to Main Page to Login", font=("Arial", 12), bg='#D0E7F9').pack()

    # Method to populate inventory
    def populate_inventory(self):
        """
        Populate the inventory list.
        """
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE quantity > 0")
        books = cursor.fetchall()

        for book in books:
            self.inventory_tree.insert("", "end", text=book[0], values=(book[1], book[2], book[5], book[6]))

    # Method to refresh inventory
    def refresh_inventory(self):
        """
        Refresh the inventory list.
        """
        # Clear existing items in the inventory treeview
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        # Repopulate the inventory treeview with updated data
        self.populate_inventory()

    # Method to open sell page
    def open_sell_page(self):
        """
        Open the sell page.
        """
        sell_window = tk.Toplevel(self.master)
        sell_window.title("ReRead - Sell Book")
        sell_window.configure(bg='#F7F7F7')
        SellPage(sell_window, self.inventory_db_connection)

    # Method to add book to cart
    def add_to_cart(self):
        """
        Add book to cart.
        """
        # Get the selected item from the inventory treeview
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to add to cart.")
            return

        # Extract book details from the selected item
        book_id = self.inventory_tree.item(selected_item, "text")
        book_title = self.inventory_tree.item(selected_item, "values")[0]
        book_author = self.inventory_tree.item(selected_item, "values")[1]
        book_price = self.inventory_tree.item(selected_item, "values")[2]
        book_quantity = int(self.inventory_tree.item(selected_item, "values")[3])

        if book_quantity <= 0:
            messagebox.showerror("Error", "This book is out of stock.")
            return

        # Update the inventory (subtract 1 from quantity)
        new_quantity = book_quantity - 1
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_quantity, book_id))
        self.inventory_db_connection.commit()

        # Add the book to the cart list
        self.cart.append({
            "id": book_id,
            "title": book_title,
            "author": book_author,
            "price": book_price
        })

        messagebox.showinfo("Success", f"Book '{book_title}' added to cart.")

# Cart Page Class
class CartPage:
    def __init__(self, master, cart, db_connection, inventory_db_connection, clear_cart2):
        """
        Initialize the cart page.

        Args:
            master (tk.Tk): The master Tkinter window.
            cart (list): The cart.
            db_connection: SQLite database connection for user data.
            inventory_db_connection: SQLite database connection for inventory data.
            clear_cart2 (function): Function to clear the cart.
        """
        # Initialize attributes
        self.master = master
        self.cart = cart
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.clear_cart2 = clear_cart2

        # Create a Treeview to display cart items
        self.cart_tree = ttk.Treeview(master, columns=("Title", "Author", "Price"), show="headings")
        self.cart_tree.heading("Title", text="Title")
        self.cart_tree.heading("Author", text="Author")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.pack(padx=10, pady=10)

        # Display cart items
        self.display_cart_items()

        # Checkout button
        checkout_button = tk.Button(master, text="Checkout", command=self.checkout, font=("Arial", 12),
                                    bg='#007BFF', fg='white')
        checkout_button.pack(pady=10)

    # Method to display cart items
    def display_cart_items(self):
        """
        Display items in the cart.
        """
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(item['title'], item['author'], item['price']))

    # Method to checkout
    def checkout(self):
        """
        Checkout the items in the cart.
        """
        # Insert cart items into user_purchases table
        cursor = self.db_connection.cursor()
        for item in self.cart:
            cursor.execute("INSERT INTO user_purchases (user_id, book_title, author, price, quantity) "
                           "VALUES (?, ?, ?, ?, ?)", (userID, item['title'], item['author'], item['price'], 1))
        self.db_connection.commit()
        self.clear_cart2()
        messagebox.showinfo("Success", "Checkout successful!")
        self.master.destroy()

# Registration Page Class
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
        # Initialize attributes
        self.master = master
        self.db_connection = db_connection
        self.master.title("ReRead - Registration")
        self.master.configure(background='#F7F7F7')

        join_label = tk.Label(self.master, text="Join Us!", font=("Arial", 16), bg='#F7F7F7')
        join_label.pack(pady=10)
        # Load and display the login image

        login_image = Image.open("login.png")
        resized_login_image = login_image.resize((200, 200))
        login_photo = ImageTk.PhotoImage(resized_login_image)

        login_label = tk.Label(master, image=login_photo, bg='#F7F7F7')
        login_label.image = login_photo
        login_label.pack()

        # Labels and Entry Widgets
        tk.Label(master, text="Username:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.username_entry = tk.Entry(master, font=("Arial", 12))
        self.username_entry.pack()

        tk.Label(master, text="Password:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.password_entry = tk.Entry(master, show="*", font=("Arial", 12))
        self.password_entry.pack()

        # Register Button
        register_button = tk.Button(master, text="Register", command=self.register_user, font=("Arial", 12),
                                    bg='#007BFF', fg='white')
        register_button.pack(pady=10)

    # Method to register user
    def register_user(self):
        """
        Register a new user.
        """
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

        tk.messagebox.showinfo("Success", "Registration successful!")
        logged_in = True

        # Clear entry fields after registration
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

# Login Page Class
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
        # Initialize attributes
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
        self.master.title("ReRead - Login")
        self.master.configure(background='#F7F7F7')

        welcomeb_label = tk.Label(self.master, text="Welcome Back!", font=("Arial", 16), bg='#F7F7F7')
        welcomeb_label.pack(pady=10)

        # Load and display the login image

        login_image = Image.open("login.png")
        resized_login_image = login_image.resize((200, 200))
        login_photo = ImageTk.PhotoImage(resized_login_image)

        login_label = tk.Label(master, image=login_photo, bg='#F7F7F7')
        login_label.image = login_photo
        login_label.pack()

        # Labels and Entry Widgets
        tk.Label(master, text="Username:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.username_entry = tk.Entry(master, font=("Arial", 12))
        self.username_entry.pack()

        tk.Label(master, text="Password:", font=("Arial", 12), bg='#F7F7F7').pack()
        self.password_entry = tk.Entry(master, show="*", font=("Arial", 12))
        self.password_entry.pack()

        # Login Button
        login_button = tk.Button(master, text="Login", command=self.login_user, font=("Arial", 12),
                                 bg='#007BFF', fg='white')
        login_button.pack(pady=10)

    # Method to login user
    def login_user(self):
        """
        Log in the user.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            tk.messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check if username exists
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            global logged_in, userID
            logged_in = True
            userID = user[0]  # Set the user ID to the logged-in user's ID
            tk.messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()
        else:
            tk.messagebox.showerror("Error", "Invalid username or password. Please try again.")

# Function to open the main page
def main():
    """
    Open the main page.
    """
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    db_connection = sqlite3.connect("user.db")
    inventory_db_connection = sqlite3.connect("inventory.db")
    main_page = MainPage(root, db_connection, inventory_db_connection)
    root.mainloop()

# Run the application
if __name__ == "__main__":
    main()
