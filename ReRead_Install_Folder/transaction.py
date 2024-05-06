"""
Name: transaction.py
Authors: Michael Coughlin,
Date Last Updated: April 20, 2024
Description: Class file for a transaction
"""

class transaction:
    def __init__(self, seller, buyer, book, price, tDate):
        self.seller = seller
        self.buyer = buyer
        self.book = book
        self.price = price
        self.tDate = tDate
