"""WAV playback using standard-library Windows APIs or OS player commands."""
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox


def player_command(platform, find=shutil.which):
    if platform == 'darwin':
        name = 'afplay'
    elif platform.startswith('linux'):
        name = 'aplay'
    else:
        return None
    return find(name)


def open_player():
    window = tk.Toplevel()
    window.title('WAV player')
    path = None
    process = None
    generation = 0
    status = tk.Label(window, text='Choose a WAV file')
    status.pack(padx=12, pady=8)

    def stop():
        nonlocal process, generation
        generation += 1
        if sys.platform == 'win32':
            import winsound
            winsound.PlaySound(None, 0)
        elif process is not None and process.poll() is None:
            process.terminate()
        process = None
        status.config(text='Stopped')

    def choose():
        nonlocal path
        selected = filedialog.askopenfilename(parent=window, filetypes=[('WAV audio', '*.wav'), ('All files', '*')])
        if selected:
            stop()
            path = selected
            status.config(text=path)

    def play():
        nonlocal process, generation
        if not path:
            messagebox.showinfo('WAV player', 'Choose a WAV file first.', parent=window)
            return
        stop()
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
                status.config(text='Playing: ' + path)
                return
            command = player_command(sys.platform)
            if not command:
                messagebox.showerror('Audio unavailable', 'No supported system player found (Linux: aplay; macOS: afplay).', parent=window)
                return
            process = subprocess.Popen([command, path], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except (OSError, RuntimeError) as exc:
            messagebox.showerror('Playback failed', str(exc), parent=window)
            return
        status.config(text='Playing: ' + path)
        current = generation
        active = process
        def wait():
            _, error = active.communicate()
            # Tk calls remain on the main thread; poll the result below.
            results.append((active.returncode, error.decode(errors='replace').strip()))
        results = []
        threading.Thread(target=wait, daemon=True).start()
        def poll():
            if current != generation:
                return
            if not results:
                window.after(100, poll)
                return
            code, error = results[0]
            status.config(text='Finished' if code == 0 else 'Playback failed: ' + (error or str(code)))
        window.after(100, poll)

    tk.Button(window, text='Choose WAV', command=choose).pack(fill='x', padx=12)
    tk.Button(window, text='Play', command=play).pack(fill='x', padx=12)
    tk.Button(window, text='Stop', command=stop).pack(fill='x', padx=12, pady=(0, 8))
    def close():
        stop()
        window.destroy()
    window.protocol('WM_DELETE_WINDOW', close)
