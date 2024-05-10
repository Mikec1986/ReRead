"""
Name: user.py
Authors: Michael Coughlin, Leah Mattingly, Aubrie McIntyre, Perrin Brumfield, Gautam Mehla
Date Last Updated: May 9th, 2024
Description: Class file for the User
"""

class User:
    """
    User class when registering a new user
    """
    def __init__(self, userID, username, password):
        self.userID = userID
        self.username = username
        self.password = password
