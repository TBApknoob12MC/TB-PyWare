import importlib.util
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import Mock, patch

# Core logic can be tested on headless Python installations without Tk.
try:
    import tkinter
except ModuleNotFoundError:
    import types
    tkinter = types.ModuleType('tkinter')
    tkinter.Tk = Mock()
    for name in ('filedialog', 'messagebox', 'scrolledtext'):
        module = types.ModuleType('tkinter.' + name)
        setattr(tkinter, name, module)
        sys.modules[module.__name__] = module
    tkinter.filedialog.askopenfilename = Mock()
    sys.modules['tkinter'] = tkinter
    turtle = types.ModuleType('turtle')
    for name in ('forward', 'backward', 'right', 'left', 'penup', 'pendown', 'mainloop'):
        setattr(turtle, name, Mock())
    sys.modules['turtle'] = turtle

import app
import process_runner
import ttsInterpreter
import Pyde
import completion
import games
import audio_player


class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(app.calculate('-(2 + 3) * 4 / 2'), -10)
        self.assertEqual(app.calculate('7 // 2 + 7 % 2'), 4)

    def test_rejects_code(self):
        for expression in ('__import__("os")', '2 ** 100', 'True', 'x'):
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                app.calculate(expression)

    def test_errors_propagate(self):
        with self.assertRaises(ZeroDivisionError):
            app.calculate('1 / 0')
        with self.assertRaises(SyntaxError):
            app.calculate('1 +')


class TurtleTests(unittest.TestCase):
    def test_all_commands_and_ignored_characters(self):
        target = Mock()
        ttsInterpreter.run_program('FB+-[]M ?', target)
        target.forward.assert_called_once_with(10)
        target.backward.assert_called_once_with(10)
        target.right.assert_called_once_with(10)
        target.left.assert_called_once_with(10)
        target.penup.assert_called_once_with()
        target.pendown.assert_called_once_with()
        target.mainloop.assert_called_once_with()

    @patch('ttsInterpreter.filedialog.askopenfilename', return_value='')
    @patch('ttsInterpreter.tk.Tk')
    def test_cancel(self, root, dialog):
        ttsInterpreter.main()
        root.return_value.destroy.assert_called_once_with()


class ProcessTests(unittest.TestCase):
    def test_path_with_spaces_and_output(self):
        class Widget:
            def __init__(self):
                self.callbacks = []
                self.text = ''
            def after(self, delay, callback):
                self.callbacks.append(callback)
            def insert(self, index, text):
                self.text += text
            def see(self, index):
                pass
        widget = Widget()
        process_runner.run_process(widget, [sys.executable, '-c', 'import sys; print(sys.argv[1])', 'a b; echo injected'])
        deadline = time.monotonic() + 5
        while widget.callbacks and time.monotonic() < deadline:
            widget.callbacks.pop(0)()
            time.sleep(.01)
        self.assertIn('a b; echo injected', widget.text)
        self.assertIn('[Exit code: 0]', widget.text)
        self.assertFalse(widget.callbacks)

    def test_import_launcher_does_not_create_window(self):
        path = Path(__file__).resolve().parents[1] / 'OS-maincode.py'
        spec = importlib.util.spec_from_file_location('launcher', path)
        with patch('tkinter.Tk', side_effect=AssertionError('unexpected GUI')):
            spec.loader.exec_module(importlib.util.module_from_spec(spec))


class FeatureTests(unittest.TestCase):
    def test_completion_is_static_and_sorted(self):
        result = completion.complete('alphabet = 2\nalpha = alphabet', 'alph')
        self.assertEqual(result, ['alpha', 'alphabet'])
        self.assertIn('print', completion.complete('', 'pri'))
        self.assertEqual(completion.complete('', 'os.'), [])
        self.assertEqual(completion.complete('', ''), [])

    def test_tic_tac_toe_results(self):
        self.assertEqual(games.winner(['X', 'X', 'X', '', 'O', '', 'O', '', '']), 'X')
        self.assertEqual(games.winner(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']), 'draw')
        self.assertIsNone(games.winner(['X', '', '', '', '', '', '', '', '']))

    def test_audio_platform_detection(self):
        self.assertEqual(audio_player.player_command('linux', lambda name: '/bin/' + name), '/bin/aplay')
        self.assertEqual(audio_player.player_command('darwin', lambda name: '/bin/' + name), '/bin/afplay')
        self.assertIsNone(audio_player.player_command('other', lambda name: name))
        self.assertIsNone(audio_player.player_command('linux', lambda name: None))


if __name__ == '__main__':
    unittest.main()
