"""
Name: book.py
Authors: Michael Coughlin,
Date Last Updated: April 20, 2024
Description: Class file for books
"""

class Book:
    def __init__(self, title, author, ISBN, condition, price):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.condition = condition
        self.price = price
