import tkinter as tk

class RereadApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Reread - Online Bookstore")

        # Header
        self.search_label = tk.Label(master, text="Welcome to ReRead!", font=("Arial", 16))
        self.search_label.pack()
        
        # Introduction
        self.intro_text = """
        Where the love for books meets the joy of recycling! 
        Dive into our virtual bookstore, where every page holds a story and every purchase breathes new life into pre-loved books.
        Search for your next literary adventure, add favorites to your cart, and embark on a journey through the endless shelves of knowledge.
        Let's rediscover the magic of reading while also caring for our planet. Happy browsing!
        """
        self.intro_label = tk.Label(master, text=self.intro_text, wraplength=400,font=("Arial", 12), justify="center")
        self.intro_label.pack() 

        # Navigation buttons
        search_button = tk.Button(master, text="Search Inventory", command=self.show_inventory_page, font=("Arial", 12))
        search_button.pack(pady=10)

        view_cart_button = tk.Button(master, text="View Cart", command=self.show_cart_page, font=("Arial", 12))
        view_cart_button.pack()

        self.current_frame = None

    def show_inventory_page(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        # Display inventory page elements
        search_entry = tk.Entry(self.current_frame, font=("Arial", 12))
        search_entry.pack()

        search_button = tk.Button(self.current_frame, text="Search", command=self.search_books, font=("Arial", 12))
        search_button.pack()

        book_listbox = tk.Listbox(self.current_frame, font=("Arial", 12))
        book_listbox.pack()

        add_to_cart_button = tk.Button(self.current_frame, text="Add to Cart", command=self.add_to_cart, font=("Arial", 12))
        add_to_cart_button.pack()

        back_button = tk.Button(self.current_frame, text="Back to Main Page", command=self.show_main_page, font=("Arial", 12))
        back_button.pack(pady=10)

    def show_cart_page(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        # Display cart page elements
        cart_label = tk.Label(self.current_frame, text="Your Cart", font=("Arial", 16))
        cart_label.pack()

        cart_listbox = tk.Listbox(self.current_frame, font=("Arial", 12))
        cart_listbox.pack()

        checkout_button = tk.Button(self.current_frame, text="Checkout", command=self.checkout, font=("Arial", 12))
        checkout_button.pack()

        back_button = tk.Button(self.current_frame, text="Back to Main Page", command=self.show_main_page, font=("Arial", 12))
        back_button.pack(pady=10)

    def search_books(self):
        # Implement search functionality here
        pass

    def add_to_cart(self):
        # Implement adding selected book to cart
        pass

    def checkout(self):
        # Implement checkout functionality
        pass

    def show_main_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.__init__(self.master)

def main():
    root = tk.Tk()
    app = RereadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
