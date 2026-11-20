"""Interpret the single-character Turtle Script language."""
import turtle
import tkinter as tk
from tkinter import filedialog, messagebox


def run_program(program, target=turtle):
    commands = {'F': lambda: target.forward(10), 'B': lambda: target.backward(10),
                '+': lambda: target.right(10), '-': lambda: target.left(10),
                '[': target.penup, ']': target.pendown, 'M': target.mainloop}
    for char in program:
        if char in commands:
            commands[char]()


def main():
    root = tk.Tk()
    root.withdraw()
    try:
        path = filedialog.askopenfilename(parent=root, filetypes=[('Turtle scripts', '*.ts')])
        if not path:
            return
        try:
            with open(path, encoding='utf-8') as file:
                program = file.read()
        except (OSError, UnicodeError) as exc:
            messagebox.showerror('Open failed', str(exc), parent=root)
            return
        run_program(program)
    finally:
        root.destroy()


if __name__ == '__main__':
    main()
