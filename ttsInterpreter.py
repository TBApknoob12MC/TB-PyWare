import turtle
import tkinter.filedialog as tk
commands = {
    "F": turtle.forward,
    "B": turtle.backward,
    "+": turtle.right,
    "-": turtle.left,
    "[": turtle.penup,
    "]": turtle.pendown,
    "M": turtle.mainloop
}

# Load in our program from a file
app=tk.askopenfilename(filetypes=[(' Turtle Scripts','*.ts')])
with open(app, "r") as f:
    program = f.read()

# Run the program by iterating through each character and running the corresponding command
for char in program:
    if char in commands:
        commands[char](10)