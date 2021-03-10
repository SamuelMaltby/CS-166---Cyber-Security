"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""

# create setup for employees
class Employee:

    def __init__(self, username, password, access):
        self.username = username
        self.password = password
        self.access = access