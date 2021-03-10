"""
Sam Maltby
CS 166 - Cybersecurity Principles
12/1/2020
Lab 8.0 - Company Intranet System
This project runs a flask web application with SQLite
users can login or create an account. The passwords are hashed
using SHA-256 and a 40 character length randomized salt.

"""

import hashlib
import os
import random

# Variables for strong password testing
PASS_MIN_LENGTH = 8
PASS_MAX_LENGTH = 25
SPECIAL_CHAR = '!@#$%^&*'


# Hash user entered password
def hash_pass(text):
    salt_size = 40  # define salt length
    salt = os.urandom(salt_size)  # create random salt
    encode = text.encode('utf-8')
    hashable = salt + encode  # add salt to password
    this_hash = hashlib.sha256(hashable).hexdigest()  # hash both salt and password
    this_hash = this_hash.encode('utf-8')
    return salt + this_hash  # return hashed and salted password


# Check user entered password vs. password stored in databse
def authenticate(stored, text):
    salt_length = 40
    salt = stored[:salt_length]  # get salt from stored password
    stored_hash = stored[salt_length:]  # get stored hashed password
    stored_hash = stored_hash.decode('utf-8')  # decode hashed password
    encode = text.encode('utf-8')
    hashable = salt + encode
    this_hash = hashlib.sha256(hashable).hexdigest()
    return this_hash == stored_hash  # return comparison of stored and entered password


# Test if user entered password is strong enough
def password_test(password):
    if password.isalnum() or password.isalpha():  # check if password is all upper or lowercase letters
        return False
    if len(password) < PASS_MIN_LENGTH:  # check if password is too short
        return False
    if len(password) > PASS_MAX_LENGTH:  # check if password is too long
        return False

    # set check variables to false for verification
    check_special = False
    has_upper = False
    has_lower = False
    has_num = False

    # check each character in the password
    for char in password:
        if char in SPECIAL_CHAR:  # check is password has a special character
            check_special = True
        if char.isupper():  # check if password has a uppercase letter
            has_upper = True
        if char.islower():  # check if password has a lowercase letter
            has_lower = True
        if char.isdigit():  # check if password has a number
            has_num = True
    if not check_special or \
            not has_upper or \
            not has_lower or \
            not has_num:
        return False  # if password doesnt have all, return false
    else:
        return True


# Generate a strong password for user
def strong_password():
    LENGTH = 16  # set length to 16
    # list of all numbers
    NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # list of all uppercase letters
    UPPERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # list of all lowercase letters
    LOWERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # list of special characters
    SPECIALS =['!', '@', '#', '$', '%', '^', '&', '*']

    word_length = 0
    password = ''
    # generate password
    while word_length < LENGTH:
        num_random = random.choice(NUMS)
        upper_random = random.choice(UPPERS)
        lowers_random = random.choice(LOWERS)
        specials_random = random.choice(SPECIALS)
        # add one from each list
        together = num_random + upper_random + lowers_random + specials_random
        # add 4 characters to password
        password += together
        # run until password is 16 characters long
        word_length += 4

    return password  # return strong password


