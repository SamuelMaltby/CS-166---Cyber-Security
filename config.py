"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""

# activate debugger when running app
DEBUG = True
SC = ";"
# allow pages to reload
TEMPLATES_AUTO_RELOAD = True
# interact with database
DB_FILE = 'user.db'
# computer generated random secret key
SECRET_KEY = '\xcaB\x94\xda\xb88\xa9#\x8e\xb7\xf7\xdb{\xf8\xbfLm1?\xc1\x08:G\x8d'
display = {}

