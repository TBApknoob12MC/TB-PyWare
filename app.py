"""Small Tk utilities used by the launcher."""
import ast
import operator
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path

from process_runner import run_process
import sys


def calculate(expression):
    """Evaluate basic arithmetic without executing Python code."""
    binary = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod}
    unary = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary:
            return binary[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary:
            return unary[type(node.op)](visit(node.operand))
        raise ValueError('Only basic arithmetic is supported')
    return visit(ast.parse(expression.strip(), mode='eval').body)


def mainx():
    calc = tk.Toplevel()
    calc.title('SimpleCalc')
    entry = tk.Entry(calc, width=30)
    entry.pack()
    def equal():
        try:
            result = calculate(entry.get())
        except (ValueError, SyntaxError, ArithmeticError, OverflowError) as exc:
            messagebox.showerror('Calculation failed', str(exc), parent=calc)
            return
        entry.delete(0, 'end')
        entry.insert(0, str(result))
    tk.Button(calc, text='=', command=equal).pack()


def mainy():
    window = tk.Toplevel()
    window.title('HTML Editor - index.html')
    editor = scrolledtext.ScrolledText(window, width=70, height=20)
    editor.pack(fill='both', expand=True)
    path = Path('index.html')
    try:
        text = path.read_text(encoding='utf-8') if path.exists() else '<html>\n<body>\n</body>\n</html>'
        editor.insert('1.0', text)
    except (OSError, UnicodeError) as exc:
        messagebox.showerror('Open failed', str(exc), parent=window)
    def save():
        try:
            path.write_text(editor.get('1.0', 'end-1c'), encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            messagebox.showerror('Save failed', str(exc), parent=window)
    tk.Button(window, text='Save', command=save).pack()


def mainz():
    window = tk.Toplevel()
    window.title('PyConsole')
    tk.Label(window, text='Runs Python code in a separate process; interactive input is not supported.').pack()
    code = tk.Text(window, height=8, width=60)
    code.pack()
    output = scrolledtext.ScrolledText(window, height=10, width=60)
    output.pack()
    tk.Button(window, text='Run', command=lambda: run_process(output, [sys.executable, '-c', code.get('1.0', 'end-1c')])).pack()


def maina():
    window = tk.Toplevel()
    window.title('FunWriter')
    scrolledtext.ScrolledText(window, wrap='word', undo=True).pack(fill='both', expand=True)


def cco():
    window = tk.Toplevel()
    window.title('GClock')
    label = tk.Label(window, fg='white', bg='black')
    label.pack()
    def update():
        label.configure(text=time.strftime('%H:%M:%S'))
        window.after(1000, update)
    update()
