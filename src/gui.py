'''
This module is the GUI.
'''

import tkinter as tk
from tkinter import Tk, Toplevel, filedialog, scrolledtext
from tkinter.scrolledtext import ScrolledText

from src.orchestrator import OCRController


class MyGUI:
    def __init__(self, root: Tk) -> None:
        self.root: Tk = root
        root.title("BX's OCR Application")
        root.geometry("600x600")
        self.label = tk.Label(self.root, text="Welcome", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.log: ScrolledText = scrolledtext.ScrolledText(self.root, height=12, font=('Arial', 14))
        self.log.pack(padx=10, pady=2)

        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, pady=0, padx=0)

        self.button = tk.Button(master=left_frame, text="Add PDF to queue", command=self.add_pdf, font=('Arial', 16))
        self.button.pack(padx=2, pady=0)

        self.run_button = tk.Button(master=left_frame, text="Process PDF(s)", command=self.overlay, font=('Arial', 16))
        self.run_button.pack(padx=20, pady=10)

        self.button = tk.Button(left_frame, text="What is this?", command=self.display_info, font=('Arial', 16))
        self.button.pack(padx=20, pady=10)

        self.label = tk.Label(self.root, text="Queue", font=('Arial, 13'))
        self.label.pack(padx=1, pady=0)

        self.listbox = tk.Listbox(self.root, height=10, width=10)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH)

        self.pdf_queue: list = []
        self.info_window = None # pyright: ignore[reportAttributeAccessIssue]

    def display_info(self):
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.lift() # visibility
            self.info_window.focus_force() # input focus (mouse is focused on here)
        else:
            self.info_window: Toplevel = tk.Toplevel(self.root)
            readmetext: str = ("This app recognizes texts from images using a"
            " publicly available neural net called Tesseract.\n"
            "Honestly, I have no idea how it works.\n" 
            "\nGenerally, this process is known as Optical Character Recognition (OCR)."
            "\n It runs entirely on your CPU, meaning nothing is uploaded to the internet."
            "\n I hope it brings convenience to you.")
            self.info_window.title("What is this?")
            self.info_window.geometry("800x200")
            label = tk.Label(self.info_window, text=readmetext, font=('Arial', 13))
            label.pack(padx=10, pady=10)

            self.info_window.protocol("WM_DELETE_WINDOW", 
            self.delete_info_window) # pyright: ignore[reportUndefinedVariable]
    
    def delete_info_window(self):
        self.info_window.destroy()
        self.info_window = None # pyright: ignore[reportAttributeAccessIssue]
    
    def add_pdf(self):
        '''
        Adds a PDF to the queue
        '''

        pdf_name = filedialog.askopenfilename(title="Select a PDF file")
        self.pdf_queue.append(pdf_name)
        self.listbox.insert(tk.END, pdf_name)
        self._log_message(f"Added {pdf_name} to queue.")
    
    def remove_pdf(self):
        '''
        Removes a PDF from the queue
        '''

        self.pdf_queue.pop(0)
        self.listbox.delete(0)

    
    def _log_message(self, text: str):
        '''
        Writes a message to the scrollabletextbox
        '''

        self.log.insert(tk.END, text + '\n')
        self.log.see(tk.END)
    
    def append_message(self, text: str):
        '''
        Thread-safe approach to write messages.
        .after writes on the main thread only
        '''

        self.root.after(0,lambda: self._log_message(text))
        # a lambda is a small anonymous function with no name.
        # used when you want to pass specific behaviour as a callback functions,
        #  but the behaviour is so simple and specific it will likely never be reused.
    
    def complete_callback(self, text: str):
        self.append_message(text)
        self.remove_pdf()

        if self.listbox.size == 0:
            self.run_button.config(state=tk.NORMAL, text = "Process PDF(s)")

    def overlay(self):
        '''
        Runs the orchestrator logic to overlay a file
        '''
        
        if not self.pdf_queue:
            self.append_message("⚠️ Queue is empty")
        
        self.run_button.config(state=tk.DISABLED, text = "⏳ Processing...")
        import threading
        controller= OCRController(self.append_message, self.complete_callback, self.pdf_queue.copy())
        thread = threading.Thread(target=controller.process_queue, daemon=True)
        thread.start()



def main():
    root = tk.Tk() # the main window of the application
    app = MyGUI(root)
    app.root.mainloop()

if __name__ == "__main__": # checks if the current file is the entry point
    main()