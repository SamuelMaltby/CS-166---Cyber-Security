"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""

import traceback
from intranet import app

# Run the Flask app

if __name__ == '__main__':
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()
