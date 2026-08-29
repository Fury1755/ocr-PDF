'''
This module is the GUI.
'''

from tkinter import Tk


import tkinter as tk

class MyGUI:

    def __init__(self, root: Tk) -> None:
        self.root: Tk = root
        root.title("Happy Hard Window")
        root.geometry("600x600")
        self.label = tk.Label(self.root, text="hihi", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)
        self.button = tk.Button(self.root, text="What is this?")
        self.button.pack(padx=20, pady=20)

def main():
    root = tk.Tk() # the main window of the application
    app = MyGUI(root)
    app.root.mainloop()

if __name__ == "__main__": # checks if the current file is the entry point
    main()