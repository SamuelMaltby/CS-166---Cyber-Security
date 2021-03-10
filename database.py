"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""
import sqlite3
from security import hash_pass, authenticate, password_test
from flask import Flask, render_template, request, url_for, flash, redirect


def create_db():
    # Initialize database
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users 
                    (
                    username text, 
                    password text, 
                    access text,
                    unique (username)
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def dummy_users():
    # Add test users to database
    password1 = 'password1'
    password1 = hash_pass(password1)
    password2 = 'password2'
    password2 = hash_pass(password2)
    password3 = 'password3'
    password3 = hash_pass(password3)
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        employees = [('username1', password1, 'admin'),
                     ('username2', password2, 'limited'),
                     ('username3', password3, 'none')
                     ]
        c.executemany("INSERT INTO users VALUES (?, ?, ?)", employees)
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def user_login(username, password):

    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        search = (username,)
        c.execute('SELECT * FROM users WHERE username=?', search)
        check = c.fetchone()
        if check is not None:
            c.execute('SELECT * FROM users WHERE username=?', search)
            stored_pass = c.fetchone()[1]
            true_hash = authenticate(stored_pass, password)

            if not true_hash:
                return False
            else:
                return True
    except KeyError:
        pass
    return False


def get_access(username):
    access = None
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        search = (username,)
        c.execute('SELECT * FROM users WHERE username=?', search)
        access = c.fetchone()[2]
        return access
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
        return access
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def add_user(data_to_insert, password):

    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.executemany("INSERT INTO users VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Username already exists, choose another.")
    if not password_test(password):
        print('Need a stronger password')
    else:
        print("Success")


create_db()  # Create the database upon running the app
dummy_users()
