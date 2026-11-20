"""Entry point for the TB-PyWare launcher."""
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import app
import audio_player
import games
from process_runner import run_process


def main():
    root = tk.Tk()
    root.title('TB-PyWare 2023.1')
    background = tk.Label(root, borderwidth=0)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()
    wallpaper = None
    greeting = tk.Label(root, text='Welcome to OS')
    greeting.pack()
    output = tk.Text(root)
    output.pack()
    settings = Path('xy.txt')
    try:
        if settings.is_file():
            greeting.config(text=settings.read_text(encoding='utf-8'))
    except (OSError, UnicodeError) as exc:
        messagebox.showerror('Settings error', str(exc), parent=root)

    def launch():
        path = filedialog.askopenfilename(parent=root, filetypes=[('Python files', '*.py')])
        if path:
            run_process(output, [sys.executable, path])

    def choose_wallpaper():
        nonlocal wallpaper
        path = filedialog.askopenfilename(parent=root, filetypes=[('PNG and GIF images', '*.png *.gif')])
        if not path:
            return
        try:
            image = tk.PhotoImage(master=root, file=path)
        except tk.TclError as exc:
            messagebox.showerror('Wallpaper failed', str(exc), parent=root)
            return
        wallpaper = image  # Keep a reference for Tk.
        background.config(image=wallpaper)

    def clear_wallpaper():
        nonlocal wallpaper
        background.config(image='')
        wallpaper = None

    def setup():
        window = tk.Toplevel(root)
        window.title('Setup')
        tk.Label(window, text='Set the welcome message').pack()
        entry = tk.Entry(window)
        entry.insert(0, greeting.cget('text'))
        entry.pack()
        def apply():
            text = entry.get()
            try:
                settings.write_text(text, encoding='utf-8')
            except (OSError, UnicodeError) as exc:
                messagebox.showerror('Settings error', str(exc), parent=window)
                return
            greeting.config(text=text)
            window.destroy()
        tk.Button(window, text='Apply', command=apply).pack()
        tk.Button(window, text='Reset', command=lambda: (entry.delete(0, 'end'), entry.insert(0, 'Welcome to OS'))).pack()

    def close():
        if messagebox.askyesno('Exit', 'Close TB-PyWare?', parent=root):
            root.destroy()

    menu = tk.Menu(root)
    programs = tk.Menu(menu, tearoff=False)
    for label, command in [('HtmEdit', app.mainy), ('GClock', app.cco), ('PyConsole', app.mainz),
                           ('Calculator', app.mainx), ('FunWriter', app.maina), ('Setup', setup),
                           ('Softlauncher', launch), ('WAV player', audio_player.open_player),
                           ('Guess the number', games.guessing_game), ('Tic-tac-toe', games.tic_tac_toe),
                           ('Choose wallpaper', choose_wallpaper), ('Clear wallpaper', clear_wallpaper), ('Exit', close)]:
        programs.add_command(label=label, command=command)
    menu.add_cascade(label='Launch', menu=programs)
    root.config(menu=menu)
    root.protocol('WM_DELETE_WINDOW', close)
    root.mainloop()


if __name__ == '__main__':
    main()
