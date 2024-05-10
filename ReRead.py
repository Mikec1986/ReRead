"""
Name: ReRead.py
Authors: Michael Coughlin, Leah Mattingly, Aubrie McIntyre, Perrin Brumfield, Gautam Mehla
Date Last Updated: May 9th, 2024
Description: Tkinter application that facilitates the purchase and selling of used books.
Users can register, login, browse books, add books to cart, and purchase books.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from user import User
from book import Book
from PIL import Image, ImageTk

global logged_in
logged_in = False
global userID
userID = None
global cart_empty


class MainPage:
    def __init__(self, master, db_connection, inventory_db_connection, cart=None):
        """
                Initialize the main page.

                Args:
                    master (tk.Tk): The master Tkinter window.
                    db_connection: SQLite database connection for user data.
                    inventory_db_connection: SQLite database connection for inventory data.
                """
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection  # Store inventory_db_connection
        self.master.title("ReRead - Main Page")
        self.master.configure(background='#F7F7F7')  # Light grey background color
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        if cart is None:
            self.cart = []  # Initialize cart as an empty list if not provided
        else:
            self.cart = cart  # Don't recreate the cart if reopening this page

        image_path = "books.jpg"  # Adjust the path accordingly
        image = Image.open(image_path)

        # Resize the image if needed
        image = image.resize((500, 300))  # Adjust width and height as needed

        # Convert the image to a format compatible with Tkinter
        self.photo = ImageTk.PhotoImage(image)

        # Create a Label widget to display the image
        image_label = tk.Label(self.master, image=self.photo, bg='#F7F7F7')
        image_label.image = self.photo  # Keep a reference to prevent garbage collection
        image_label.pack()

        welcomea_label = tk.Label(self.master, text="Welcome to ReRead!", font=("Arial", 16), bg='#F7F7F7')
        welcomea_label.pack(pady=10)
        # Introduction
        intro_text = """
        Where the love for books meets the joy of recycling! 
        Dive into our virtual bookstore, where every page holds a story and every purchase breathes new life into pre-loved books.
        Search for your next literary adventure, add favorites to your cart, and embark on a journey through the endless shelves of knowledge.
        Let's rediscover the magic of reading while also caring for our planet. Happy browsing!
        """
        intro_label = tk.Label(master, text=intro_text, wraplength=400, justify="center", font=("Arial", 12),
                               bg='#F7F7F7')  # Set background color
        intro_label.pack()

        inventory_button = tk.Button(master, text="Inventory", command=self.open_inventory_window, font=("Arial", 12),
                                     bg='#007BFF', fg='white')  # Set button color
        inventory_button.pack(pady=5)

        if not logged_in:
            # Login and Register buttons
            login_button = tk.Button(master, text="Login", command=self.open_login_window, font=("Arial", 12),
                                     bg='#28A745', fg='white')
            login_button.pack(pady=5)

            register_button = tk.Button(master, text="Register", command=self.open_register_window, font=("Arial", 12),
                                        bg='#28A745', fg='white')
            register_button.pack(pady=5)

        if logged_in:       
            view_cart_button = tk.Button(master, text="View Cart", command=self.open_cart_window, font=("Arial", 12),
                                         bg='#007BFF', fg='white')
            view_cart_button.pack(pady=5)

            logout_button = tk.Button(master, text="Log Out", command=self.logout, font=("Arial", 12),
                                      bg='#DC3545', fg='white')
            logout_button.pack(pady=5)

    def logout(self):   
        global logged_in               
        logged_in = False   
        self.master.destroy()
        main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)

    def clear_cart(self):   
        """
        Clears the cart after checkout  
        """
        self.cart = []

    def open_inventory_window(self):
        """
        Open the inventory window.
        """
        self.master.withdraw()  # Hide the main window
        inventory_window = tk.Toplevel(self.master) # Create a new window
        inventory_window.title("ReRead - Inventory")               
        inventory_window.configure(bg='#F7F7F7')    
        inventory_window.protocol("WM_DELETE_WINDOW", self.on_inventory_window_close)                  
        InventoryPage(inventory_window, self.db_connection, self.inventory_db_connection, self.cart, self.open_cart_window) 

    def open_cart_window(self):
        """
        Open the cart window.
        """
        self.master.withdraw()  # Hide the main window
        cart_window = tk.Toplevel(self.master)  # Create a new window
        cart_window.protocol("WM_DELETE_WINDOW", self.on_cart_window_close) # Set the close window callback
        cart_window.title("ReRead - View Cart") # Set the window title
        cart_window.configure(bg='#F7F7F7') 
        CartPage(cart_window, self.cart, self.db_connection, self.inventory_db_connection, self.clear_cart)     

    def open_login_window(self):
        """
        Open the login window.
        """
        self.master.withdraw()  # Hide the main window
        login_window = tk.Toplevel(self.master) # Create a new window
        login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)   # Set the close window callback            
        login_window.title("ReRead - Login")    # Set the window title
        login_window.configure(bg='#F7F7F7')            
        LoginPage(login_window, self.db_connection, self.inventory_db_connection)       


    def open_register_window(self):
        """
        Open the registration window.
        """
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)  # Create a new window
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_window_close) # Set the close window callback
        register_window.title("ReRead - Registration")
        register_window.configure(bg='#F7F7F7')
        RegistrationPage(register_window, self.db_connection, self.inventory_db_connection)

    # Show the main window when window is closed
    def on_inventory_window_close(self):
        """
        Callback when the inventory window is closed.
        """
        self.master.destroy()   
        if logged_in:   
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection, self.cart)    
        else:
            main()

    def on_cart_window_close(self):
        """
        Callback when the cart window is closed.
        """
        self.master.destroy()   
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
        else:
            main()

    def on_register_window_close(self):
        """
        Callback when the register window is closed.
        """
        self.master.destroy()
        if logged_in:
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
        else:
            main()

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

class RegistrationPage:
    """
    Class representing the registration page.
    """

    def __init__(self, master, db_connection, inventory_db_connection):
        """
        Initialize the registration page.

        Args:
            master (tk.Tk): The master Tkinter window.
            db_connection: SQLite database connection for user data.
        """
        self.master = master
        self.db_connection = db_connection
        self.inventory_db_connection = inventory_db_connection
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

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        global logged_in

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

        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.db_connection.commit()

            # Get the last inserted row ID (auto-incremented)
            user_id = cursor.lastrowid

            # Format the user ID to a four-digit number
            user_id_four_digits = '{:04d}'.format(user_id)

            #Create a new user object
            new_user = User(user_id_four_digits,username,password)

            tk.messagebox.showinfo("Success", "Registration successful!")
            logged_in = True

            # Clear entry fields after registration
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            #Withdraw and destroy window after registering
            self.master.withdraw()
            self.master.destroy()
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)
            

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

    def login_user(self):
        """
        Log in the user.
        """
        username = self.username_entry.get()       
        password = self.password_entry.get()    
        global logged_in
        global userID

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Check if username and password match
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)) 
        user = cursor.fetchone()    

        if user:
            userID = user[0]
            messagebox.showinfo("Success", "Login successful!")
            logged_in = True
            self.master.withdraw()  
            self.master.destroy()
            main_page = MainPage(tk.Toplevel(), self.db_connection, self.inventory_db_connection)

        else:
            messagebox.showerror("Error", "Invalid username or password.")

class InventoryPage:
    """
    Class representing the inventory page.
    """
    def __init__(self, master, db_connection, inventory_db_connection, cart, open_cart_window):
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
        self.cart = cart
        self.open_cart_window2 = open_cart_window   
        self.master.configure(bg='#F7F7F7') 

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

        refresh_button = tk.Button(master, text="Refresh", command=self.refresh_inventory, font=("Arial", 12),
                                   bg='#007BFF', fg='white')
        refresh_button.pack(pady=10)

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

    def populate_inventory(self):
        """
         Populate the inventory list.
         """
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE quantity > 0")
        books = cursor.fetchall()

        for book in books:
        # Format the price with two decimal places and a dollar sign
            formatted_price = "${:.2f}".format(book[5])
            self.inventory_tree.insert("", "end", text=book[0], values=(book[1], book[2], formatted_price, book[6]))

    def refresh_inventory(self):
        # Clear existing items in the inventory treeview
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        # Repopulate the inventory treeview with updated data
        self.populate_inventory()

    def open_sell_page(self):
        """
        Open the sell page.
        """
        sell_window = tk.Toplevel(self.master)
        sell_window.title("ReRead - Sell Book")     
        sell_window.configure(bg='#F7F7F7')
        SellPage(sell_window, self.inventory_db_connection)
 
    def add_to_cart(self):
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
        self.inventory_db_connection = inventory_db_connection  # Store inventory_db_connection
        self.master.title("ReRead - Sell Book") # Set window title
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

        sell_button = tk.Button(master, text="Sell", command=self.sell_book, font=("Arial", 12),
                                bg='#007BFF', fg='white')
        sell_button.pack(pady=10)

    def sell_book(self):
        # Get book details from the form    
        title = self.title_entry.get()  
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        # Verify quantity and  is a whole number
        try:
            quantity_test = int(quantity)
            price_test = float(price)
            if quantity_test < 1 or price_test < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity or price.")
            return

        # Validate input
        if not title or not author or not price or not quantity:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert book into the inventory database
        cursor = self.inventory_db_connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE title=? AND author=?", (title, author))
        repeat = cursor.fetchone()
        if repeat:
            new_quantity = int(quantity) + int(repeat[6])  # Ensure consistency by converting repeat[6] to int
            cursor.execute("UPDATE inventory SET quantity=? WHERE title=? AND author=?", (new_quantity, title, author))
        else:
            cursor.execute("INSERT INTO inventory (title, author, price, quantity) VALUES (?, ?, ?, ?)",
                        (title, author, price, quantity))

        self.inventory_db_connection.commit()
        messagebox.showinfo("Success", "Book added to inventory successfully!")
        self.master.destroy()


class CartPage:
    def __init__(self, master, cart, db_connection, inventory_db_connection, clear_cart2):
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


    def display_cart_items(self):
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(item['title'], item['author'], item['price']))

    def checkout(self):
        # Insert cart items into user_purchases table
        cursor = self.db_connection.cursor()
        for item in self.cart:
            cursor.execute("INSERT INTO user_purchases (user_id, book_title, author, price, quantity) "
                           "VALUES (?, ?, ?, ?, ?)", (userID, item['title'], item['author'], item['price'], 1))
        self.db_connection.commit()
        self.clear_cart2()
        messagebox.showinfo("Success", "Checkout successful!")
        self.master.destroy()


def main():
    # Create a SQLite database connection
    db_connection = sqlite3.connect("user_database.db")
    cursor = db_connection.cursor()

    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    # Create users table if not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_purchases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        item_no INTEGER,
                        book_title TEXT,
                        author TEXT,
                        price REAL,
                        quantity INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

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
    root.mainloop()



if __name__ == "__main__":
    main()
