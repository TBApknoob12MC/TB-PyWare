"""A small editor for Python, HTML and Turtle Script files."""
import sys
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from process_runner import run_process
from completion import complete


def main():
    root = tk.Tk()
    root.title('new - PyDE')
    path = None
    editor = tk.Text(root, height=20, width=100, undo=True)
    editor.pack()
    output = tk.Text(root, height=12, width=100)
    output.pack()

    def confirm_discard():
        return not editor.edit_modified() or messagebox.askyesno(
            'Unsaved changes', 'Discard unsaved changes?', parent=root)

    def open_file():
        nonlocal path
        if not confirm_discard():
            return
        selected = filedialog.askopenfilename(parent=root, filetypes=[('Supported files', '*.py *.html *.ts'), ('All files', '*')])
        if not selected:
            return
        try:
            text = Path(selected).read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            messagebox.showerror('Open failed', str(exc), parent=root)
            return
        editor.delete('1.0', 'end')
        editor.insert('1.0', text)
        editor.edit_modified(False)
        path = selected
        root.title(f'{path} - PyDE')

    def save():
        nonlocal path
        selected = filedialog.asksaveasfilename(parent=root, initialfile=Path(path).name if path else '',
            filetypes=[('Python files', '*.py'), ('HTML files', '*.html'), ('Turtle scripts', '*.ts'), ('All files', '*')])
        if not selected:
            return False
        try:
            Path(selected).write_text(editor.get('1.0', 'end-1c'), encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            messagebox.showerror('Save failed', str(exc), parent=root)
            return False
        path = selected
        editor.edit_modified(False)
        root.title(f'{path} - PyDE')
        return True

    def execute():
        if not path or editor.edit_modified():
            if not messagebox.askyesno('Save required', 'Save the current code before running?', parent=root) or not save():
                return
        if Path(path).suffix.lower() != '.py':
            messagebox.showerror('Cannot run', 'Only Python files can be run here.', parent=root)
            return
        run_process(output, [sys.executable, path])

    def show_completion(event=None):
        before = editor.get('1.0', 'insert')
        match = re.search(r'[A-Za-z_][A-Za-z_0-9]*$', before)
        if not match:
            return 'break'
        prefix = match.group()
        options = complete(editor.get('1.0', 'end-1c'), prefix)
        if not options:
            root.bell()
            return 'break'
        menu = tk.Menu(root, tearoff=False)
        def insert(word):
            # Avoid replacing text if the cursor or prefix changed while the menu was open.
            current = editor.get('insert - %d chars' % len(prefix), 'insert')
            if current == prefix:
                editor.delete('insert - %d chars' % len(prefix), 'insert')
                editor.insert('insert', word)
        for word in options[:30]:
            menu.add_command(label=word, command=lambda word=word: insert(word))
        menu.bind('<Unmap>', lambda event: menu.after_idle(menu.destroy))
        coords = editor.bbox('insert')
        x = editor.winfo_rootx() + (coords[0] if coords else 0)
        y = editor.winfo_rooty() + (coords[1] + coords[3] if coords else 0)
        menu.tk_popup(x, y)
        return 'break'

    editor.bind('<Control-space>', show_completion)

    def terminal():
        window = tk.Toplevel(root)
        window.title('Terminal (shell commands)')
        tk.Label(window, text='Commands execute in your system shell; interactive input is not supported.').pack()
        entry = tk.Entry(window, width=70)
        entry.pack()
        tk.Button(window, text='Run', command=lambda: run_process(output, entry.get(), shell=True)).pack()

    def close():
        if confirm_discard():
            root.destroy()

    menu = tk.Menu(root)
    actions = tk.Menu(menu, tearoff=False)
    for label, command in [('Execute', execute), ('Clear all', lambda: editor.delete('1.0', 'end')),
                           ('Open', open_file), ('Save as', save), ('Complete (Ctrl+Space)', show_completion), ('Terminal', terminal), ('Close', close)]:
        actions.add_command(label=label, command=command)
    menu.add_cascade(label='IO System', menu=actions)
    root.config(menu=menu)
    root.protocol('WM_DELETE_WINDOW', close)
    editor.edit_modified(False)
    root.mainloop()


if __name__ == '__main__':
    main()
