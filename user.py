"""
Name: user.py
Authors: Michael Coughlin,
Date Last Updated: May 9th, 2024
Description: Class file for the User
"""

class User:
    def __init__(self, userID, username, email, password):
        self.userID = userID
        self.username = username
        self.email = email
        self.password = password
