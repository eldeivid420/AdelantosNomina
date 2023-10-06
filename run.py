# run.py
import os
from waitress import serve
from main import application  # Import your app
import tkinter as tk
from tkinter import messagebox


# Run from the same directory as this script
this_files_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_files_dir)

# `url_prefix` is optional, but useful if you are serving app on a sub-dir
# behind a reverse-proxy.
serve(application, host='0.0.0.0', port=8080, url_prefix='/test')

root = tk.Tk()
root.title('Sistema Din Express')
