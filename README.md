# TB-PyWare

A small collection of Tk desktop utilities, an editor, and a Turtle Script interpreter.

## Requirements and launch

Use Python 3 with Tkinter installed and a graphical display. Tkinter may require a separate OS package (for example, `python3-tk` on Debian/Ubuntu). From the repository directory:

```sh
python3 OS-maincode.py       # launcher: calculator, HTML editor, clock, console, etc.
python3 Pyde.py              # standalone editor
python3 ttsInterpreter.py    # choose a Turtle Script file
python3 -m unittest discover -s tests -v
```

On Windows, use `python` in place of `python3` if appropriate. The launcher stores its welcome message in `xy.txt` in the current working directory; HtmEdit reads and writes `index.html` there. PyDE saves using UTF-8 and only executes Python files; save changes before execution.

## Code execution and limitations

Softlauncher and PyDE run selected Python files with the same permissions as the current user. PyConsole runs the entered Python code, and PyDE's terminal runs shell commands. **These are not sandboxes:** only run code and commands you trust. Output is collected asynchronously, but interactive stdin is not supported. Programs continue running independently if their window is closed; there is currently no cancellation control.

The calculator supports numbers, parentheses, unary plus/minus, and `+`, `-`, `*`, `/`, `//`, `%` only.

## Turtle Script

The interpreter reads one character at a time: `F` and `B` move forward/back 10 units, `+` and `-` turn right/left 10 degrees, `[` lifts the pen, `]` lowers it, and `M` starts the Turtle event loop. Other characters are ignored. For example, `F+F+F+F M` moves and turns four times, then keeps the window open until it is closed. Put `M` at the end, as it blocks until the Turtle window closes.

## Wallpaper, audio, completion and games

The launcher's **Choose wallpaper** uses a PNG or GIF as the launcher window background (not the system desktop wallpaper). It is displayed at its original size and is not persisted between sessions; **Clear wallpaper** removes it. Tk's image format support depends on the installed Tk version.

**WAV player** plays WAV files without third-party Python packages. Windows uses `winsound`, macOS uses the built-in `afplay` command, and Linux requires `aplay` to be installed separately and available on PATH. Playback also requires a working audio device. Stop ends playback; unsupported platforms or missing tools show an error.

In PyDE, type the beginning of a name and press **Ctrl+Space** (or choose Complete from the menu). Suggestions use Python keywords, built-in names and words already in the document. This is static word completion, not context-aware or attribute completion; it never evaluates code. Up to 30 matches are shown.

The launcher also includes **Guess the number** and local two-player **Tic-tac-toe**.
