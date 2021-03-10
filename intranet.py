"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""

from flask import Flask, render_template, request, url_for, flash, redirect
from config import display
import sqlite3
from database import user_login, get_access
from security import hash_pass, authenticate, password_test, strong_password

'''Initialize the Flask app'''
app = Flask(__name__)
'''inherit app qualities from config.py'''
app.config.from_object('config')

MAX_ATTEMPTS = 3


# Home page for web interface
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display)


# Login page on web interface
@app.route('/login', methods=['GET', 'POST'])
def login():
    attempts = 0
    MAX_ATTEMPTS = 3
    if request.method == 'POST':
        username = request.form.get('username')
        username = username.strip()
        password = request.form.get('password')
        password = password.strip()

        # access = user_login(username, password)
        while attempts < MAX_ATTEMPTS:
            try:
                success = user_login(username, password)
                if not success:
                    attempts += 1
                    flash("Invalid username or password!", 'alert-danger')
                    if attempts == MAX_ATTEMPTS:
                        flash(f"\tThat was {MAX_ATTEMPTS} invalid attempts.")
                        flash("\t** You are locked out of the system. **\n")
                        return redirect(url_for('lockout'))
                    else:
                        return redirect(url_for('login', attempts=attempts))
                if success:
                    access = get_access(username)
                    if access is not None:
                        flash("Welcome back " + username + "! You have successfully logged in.", 'alert-success')
                        if access == 'admin':
                            return redirect(url_for('menu_admin'))
                        if access == 'limited':
                            return redirect(url_for('menu_limited'))
                        if access == 'none':
                            return redirect(url_for('menu_none'))
            except KeyError:
                pass
            attempts += 1
            flash("Invalid username or password!", 'alert-danger')
            if attempts == MAX_ATTEMPTS:
                flash(f"\tThat was {MAX_ATTEMPTS} invalid attempts.")
                flash("\t** You are locked out of the system. **\n")
                return redirect(url_for('lockout'))
            else:
                return redirect(url_for('login', attempts=attempts))

    return render_template('login.html',
                           title="EmployeeLogin",
                           heading="Employee Login",
                           attempts=attempts)


# Signup page on web interface
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get entered info
    if request.method == 'POST':
        username = request.form.get('username')
        username = username.strip()
        password = request.form.get('password')
        password = password.strip()
        # Generate strong password
        if password == 'STRONG':
            password = strong_password()
            # Show user their password
            flash("Your password is: " + password, 'alert-success')
        # Hash users password
        hashed = hash_pass(password)
        access = "none"
        data_to_insert = [(username, hashed, access)]
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            # insert data into database
            c.executemany("INSERT INTO users VALUES (?, ?, ?)", data_to_insert)
            if not password_test(password):
                flash(
                    "Password is not strong enough.",
                    'alert-danger')
                return redirect(url_for('signup'))
            else:
                # Add user info to database
                conn.commit()
                flash("Success! You have created an account.", 'alert-success')
                return redirect(url_for('menu_none'))
        except sqlite3.IntegrityError:  # Error for username already in database
            pass
        flash("Username already exists, choose another.", 'alert-danger')
    # Run HTML for webpage
    return render_template('signup.html',
                           title="Create Account",
                           heading="Create Account")


# Menu page on web interface
@app.route('/menu_admin', methods=['GET', 'POST'])
def menu_admin():
    # Run HTML for webpage
    return render_template('menu_admin.html',
                           title="Menu",
                           heading="Menu")


# Menu page on web interface
@app.route('/menu_limited', methods=['GET', 'POST'])
def menu_limited():
    # Run HTML for webpage
    return render_template('menu_limited.html',
                           title="Menu",
                           heading="Menu")


# Menu page on web interface
@app.route('/menu_none', methods=['GET', 'POST'])
def menu_none():
    # Run HTML for webpage
    return render_template('menu_none.html',
                           title="Menu",
                           heading="Menu")


# Time Reporting page on web interface
@app.route('/time', methods=['GET', ])
def time():
    # Run HTML for webpage
    return render_template('time_reporting.html',
                           title="Time Repoting")


# Accounting page on web interface
@app.route('/accounting', methods=['GET', ])
def accounting():
    # Run HTML for webpage
    return render_template('accounting.html',
                           title="Accounting")


# IT Helpdesk page on web interface
@app.route('/it_help', methods=['GET', ])
def it_help():
    # Run HTML for webpage
    return render_template('it_help.html',
                           title="IT Helpdesk")


# Engineering Documents page on web interface
@app.route('/engineering_docs', methods=['GET', ])
def engineering_docs():
    # Run HTML for webpage
    return render_template('engineering_docs.html',
                           title="Engineering Documents")


# Logout page on web interface
@app.route('/logout', methods=['GET', ])
def logout():
    # Run HTML for webpage
    return render_template('logout.html')


# Locked out user page on web interface
@app.route('/Lockout', methods=['GET', ])
def lockout():
    return '** YOU HAVE BEEN LOCKED OUT OF THE SYSTEM **'

