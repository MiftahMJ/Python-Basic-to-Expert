# bot/utils.py

import random
import string
import os

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()
