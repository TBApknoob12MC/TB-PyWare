"""Small games for the launcher."""
import random
import tkinter as tk
from tkinter import messagebox


def guessing_game():
    window = tk.Toplevel()
    window.title('Guess the number')
    target = random.randint(1, 100)
    attempts = 0
    status = tk.Label(window, text='Guess a number from 1 to 100')
    status.pack(padx=10, pady=5)
    entry = tk.Entry(window)
    entry.pack(padx=10)
    def guess():
        nonlocal attempts
        try:
            number = int(entry.get())
            if not 1 <= number <= 100:
                raise ValueError
        except ValueError:
            status.config(text='Enter a whole number from 1 to 100.')
            return
        attempts += 1
        if number == target:
            status.config(text=f'Correct! You took {attempts} guesses.')
            button.config(state='disabled')
        else:
            status.config(text='Too low!' if number < target else 'Too high!')
        entry.delete(0, 'end')
    button = tk.Button(window, text='Guess', command=guess)
    button.pack(pady=5)
    entry.bind('<Return>', lambda event: guess() if button['state'] != 'disabled' else None)


def winner(board):
    """Return the winning mark, 'draw', or None for an unfinished board."""
    for a, b, c in ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)):
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return 'draw' if all(board) else None


def tic_tac_toe():
    window = tk.Toplevel()
    window.title('Tic-tac-toe (two players)')
    board = [''] * 9
    turn = 'X'
    status = tk.Label(window, text='X to play')
    status.pack()
    grid = tk.Frame(window)
    grid.pack()
    buttons = []
    def play(index):
        nonlocal turn
        if board[index] or winner(board):
            return
        board[index] = turn
        buttons[index].config(text=turn)
        result = winner(board)
        if result:
            status.config(text='Draw!' if result == 'draw' else f'{result} wins!')
        else:
            turn = 'O' if turn == 'X' else 'X'
            status.config(text=f'{turn} to play')
    for i in range(9):
        button = tk.Button(grid, text=' ', width=5, height=2, command=lambda i=i: play(i))
        button.grid(row=i // 3, column=i % 3)
        buttons.append(button)
    def reset():
        nonlocal turn
        board[:] = [''] * 9
        turn = 'X'
        status.config(text='X to play')
        for button in buttons:
            button.config(text=' ')
    tk.Button(window, text='New game', command=reset).pack(pady=5)
