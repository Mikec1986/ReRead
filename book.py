"""
Name: book.py
Authors: Michael Coughlin, Leah Mattingly, Aubrie McIntyre, Perrin Brumfield, Gautam Mehla
Date Last Updated: May 9th, 2024
Description: Class file for books
"""

class Book:
    """
    Class for Books to be sold
    """
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
