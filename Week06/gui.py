import tkinter as tk
from tkinter import Frame, Label, Button
from turtle import fill
from number_entry import IntEntry
import random

def main():
    root = tk.Tk()
    frm_main = Frame(root)
    frm_main.master.title("Dice")
    frm_main.pack(padx=3, pady=3, fill = tk.BOTH, expand=True)
    frm_main.mainloop()

if __name__  == "__main__":
    main()