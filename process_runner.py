"""Run programs without blocking Tk's event loop."""
import queue
import subprocess
import threading


def run_process(widget, args, *, shell=False):
    """Start a process and append its output to a Tk text widget.

    Stdin is closed: interactive programs are not supported.
    """
    events = queue.Queue()

    def worker():
        try:
            process = subprocess.Popen(args, shell=shell, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, errors='replace', bufsize=1)
            with process.stdout:
                for line in process.stdout:
                    events.put(line)
            process.wait()
            events.put(f'\n[Exit code: {process.returncode}]\n')
        except (OSError, ValueError) as exc:
            events.put(f'Could not start process: {exc}\n')
        finally:
            events.put(None)

    def poll():
        try:
            while True:
                item = events.get_nowait()
                if item is None:
                    return
                widget.insert('end', item)
                widget.see('end')
        except queue.Empty:
            widget.after(100, poll)

    threading.Thread(target=worker, daemon=True).start()
    widget.after(100, poll)
