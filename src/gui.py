'''
This module is the GUI.
'''

from tkinter import Tk, Toplevel


import tkinter as tk

class MyGUI:
    def __init__(self, root: Tk) -> None:
        self.root: Tk = root
        root.title("Happy Hard Window")
        root.geometry("600x600")
        self.label = tk.Label(self.root, text="hihi", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)
        self.textbox = tk.Text(self.root, height=10, font=('Arial', 12))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="What is this?", command=self.display_info, font=('Arial', 16))
        self.button.pack(padx=20, pady=20)

        self.info_window = None # pyright: ignore[reportAttributeAccessIssue]

    def display_info(self):
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.lift() # visibility
            self.info_window.focus_force() # input focus (mouse is focused on here)
        else:
            self.info_window: Toplevel = tk.Toplevel(self.root)
            readmetext: str = ("This is a small app I made.\nIt recognizes texts from images using a"
            " publicly available neural network called Tesseract.\n"
            "I have no idea how it works, but I hope it helps.\n" 
            "Generally, this process is known as Optical Character Recognition (OCR)."
            "\n It runs entirely on your CPU, meaning nothing is uploaded to the internet.")
            self.info_window.title("What is this?")
            self.info_window.geometry("800x200")
            label = tk.Label(self.info_window, text=readmetext, font=('Arial', 10))
            label.pack(padx=10, pady=10)

            self.info_window.protocol("WM_DELETE_WINDOW", 
            delete_info_window) # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    
    def delete_info_window(self):
        self.info_window.destroy()
        self.info_window = None # pyright: ignore[reportAttributeAccessIssue]
    



def main():
    root = tk.Tk() # the main window of the application
    app = MyGUI(root)
    app.root.mainloop()

if __name__ == "__main__": # checks if the current file is the entry point
    main()