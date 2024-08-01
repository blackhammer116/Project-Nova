#!/bin/bash/python3
"""
This module is responsible for the configuration of the routes to
encrypt and decrypt the data of the user.

Below are some libraries that will be used in this module
"""
import os
import subprocess
import requests
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64


salt = b'secure_salt'
iterations = 100000

def derive_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_text(text, password):
    key = ''
    if "EN_KEY.key" not in os.listdir():
        key = derive_key(password)
    #key = Fernet.generate_key()
        with open("EN_KEY.key" , "wb") as theKey:
            theKey.write(key)
    else:
        with open("EN_KEY.key", "rb") as theKey:
            key=theKey.read()
    cypher_suit = Fernet(key)
    cypher_text = cypher_suit.encrypt(text.encode()).decode()
    print(text, "\n", cypher_text)
    return cypher_text


def decrypt_text(text ,password):

    key = ''
    if "EN_KEY.key" not in os.listdir():
        key = derive_key(password)
    #key = Fernet.generate_key()
        with open("EN_KEY.key" , "wb") as theKey:
            theKey.write(key)
    else:
        with open("EN_KEY.key", "rb") as theKey:
            key=theKey.read()
    cipher_suite = Fernet(key)

    normal_text = cipher_suite.decrypt(text.encode()).decode()

    print(normal_text)
    return normal_text


if __name__=="__main__":
    encrypt_text("abebe", "123")
    d_txt = b'gAAAAABmmYsa70kYv5G6pA1L2sKk-A0tB93_sVs083sjw4mCWnXCtIE8sbTUt7Bl3JeAVNIOT73p6PuffNz_MTEsoSRG4WfUNA=='
    decrypt_text(d_txt, "123")
