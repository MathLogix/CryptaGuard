#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import time
import sys

def animate_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

txt1= " Initiating Encryption..."
txt2= " ======================================================================"
def encrypt_path():
    animate_text(txt1)
    animate_text(txt2)
    print(" Attention: DO NOT joke with this program.")
    print(" Right click on the desired file or directory and use the {Copy as path} option.")
    print(" ----------------------------------------------------------------------")
    
    path = input(" Please Enter the File or Directory Path: ")
    print(" ----------------------------------------------------------------------")

    if "\\" in path:
        path = path.replace("\\", "/")

    if '"' in path:
        path = path.replace('"', '')

    pass_from_user = input(" Please Enter Your Password: ")
    print(" ----------------------------------------------------------------------")

    password = pass_from_user.encode()

    mysalt = b'v\xaa\xf0z\xc8y\xa9\xdc\x9e\xa6\xe1\xd6\xf6\x85S\x0b'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=mysalt,
        iterations=10000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    cipher = Fernet(key)

    if os.path.isfile(path):
        with open(path, 'rb') as f:
            e_file = f.read()

        encrypted_file = cipher.encrypt(e_file)

        with open(path, 'wb') as ef:
            ef.write(encrypted_file)

        print(" File Encrypted Successfully!")
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                with open(file_path, 'rb') as f:
                    e_file = f.read()

                encrypted_file = cipher.encrypt(e_file)

                with open(file_path, 'wb') as ef:
                    ef.write(encrypted_file)

        print(" Directory Encrypted Successfully!")
    else:
        print(" Invalid Path!")

    print(" Your KEY is:", key.decode())
    print(" ----------------------------------------------------------------------")
    print(" Keep Your KEY safe & DO NOT SHARE THE KEY WITH ANYONE")
    print(" ----------------------------------------------------------------------")

txt3= " Initiating Decryption..."

def decrypt_path():
    animate_text(txt3)
    animate_text(txt2)
    print(" Right click on the desired file or directory and use the {Copy as path} option.")
    print(" ----------------------------------------------------------------------")

    path = input(" Please Enter the File or Directory Path: ")
    print(" ----------------------------------------------------------------------")

    if "\\" in path:
        path = path.replace("\\", "/")

    if '"' in path:
        path = path.replace('"', '')

    pass_from_user = input(" Please Enter Your Password: ")
    print(" ----------------------------------------------------------------------")

    password = pass_from_user.encode()

    mysalt = b'v\xaa\xf0z\xc8y\xa9\xdc\x9e\xa6\xe1\xd6\xf6\x85S\x0b'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=mysalt,
        iterations=10000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    cipher = Fernet(key)

    if os.path.isfile(path):
        with open(path, 'rb') as df:
            encrypted_data = df.read()

        decrypted_file = cipher.decrypt(encrypted_data)

        directory_path = os.path.dirname(path)
        file_format = os.path.splitext(path)[1]

        base_filename = os.path.basename(path)
        new_filename = os.path.join(directory_path, base_filename.replace(file_format, '_decrypted' + file_format))

        with open(new_filename, 'wb') as df:
            df.write(decrypted_file)

        print(" File Decrypted Successfully!")
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                with open(file_path, 'rb') as df:
                    encrypted_data = df.read()

                decrypted_file = cipher.decrypt(encrypted_data)

                directory_path = os.path.dirname(file_path)
                file_format = os.path.splitext(file_path)[1]

                base_filename = os.path.basename(file_path)
                new_filename = os.path.join(directory_path, base_filename.replace(file_format, '_decrypted' + file_format))

                with open(new_filename, 'wb') as df:
                    df.write(decrypted_file)

        print(" Directory Decrypted Successfully!")
    else:
        print(" Invalid Path!")

app = tk.Tk()
app.title("CryptaGuard")
app.geometry("370x135")

intro_label = tk.Label(app, text="Please choose one of the following programs:", font=("Helvetica", 12))
encrypt_icon = PhotoImage(file="images/encryption-icon.png")
decrypt_icon = PhotoImage(file="images/decryption-icon.png")

encrypt_button = tk.Button(app, image=encrypt_icon, command=encrypt_path)
decrypt_button = tk.Button(app, image=decrypt_icon, command=decrypt_path)

intro_label.grid(row=0, column=0, columnspan=2, padx=(5, 0), pady=(10, 10))
encrypt_button.grid(row=1, column=0, padx=(55, 50), pady=(0, 10))
decrypt_button.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

app.mainloop()

