import tkinter as tk

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title("ReRead - Main Page")
        self.master.configure(background='#D0E7F9')  # Soft blue background color

        # Introduction
        intro_text = """
        Welcome to ReRead - where the love for books meets the joy of recycling! 
        Dive into our virtual bookstore, where every page holds a story and every purchase breathes new life into pre-loved books.
        Search for your next literary adventure, add favorites to your cart, and embark on a journey through the endless shelves of knowledge.
        Let's rediscover the magic of reading while also caring for our planet. Happy browsing!
        """
        intro_label = tk.Label(master, text=intro_text, wraplength=400, justify="center", font=("Arial", 12), bg='#D0E7F9')  # Set background color
        intro_label.pack()

        # Navigation buttons
        search_button = tk.Button(master, text="Search Inventory", command=self.open_search_window, font=("Arial", 12), bg='blue',fg='white')  # Set button color
        search_button.pack(pady=10)
        

        view_cart_button = tk.Button(master, text="View Cart", command=self.open_cart_window, font=("Arial", 12),bg='blue',fg='white')
        view_cart_button.pack()

    def open_search_window(self):
        search_window = tk.Toplevel(self.master)
        search_window.title("ReRead - Search Inventory")
        search_window.configure(bg='#D0E7F9')  # Soft blue background color
        SearchPage(search_window)

    def open_cart_window(self):
        cart_window = tk.Toplevel(self.master)
        cart_window.title("ReRead - View Cart")
        cart_window.configure(bg='#D0E7F9')  # Soft blue background color
        CartPage(cart_window)

class SearchPage:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='#D0E7F9')  # Soft blue background color

        # Implement search functionality here

class CartPage:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg='#D0E7F9')  # Soft blue background color

        # Implement cart functionality here

def main():
    root = tk.Tk()
    main_page = MainPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

