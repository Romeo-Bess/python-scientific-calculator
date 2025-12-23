import tkinter as tk
import math

root = tk.Tk()
root.title("Sci Calculator")
root.geometry("450x800")
root.resizable(False, False)
root.config(bg="lightgray")  # simple clean background

# title label
title_label = tk.Label(root, text="Scientific Calculator", font=("Arial", 24, "bold"), bg="lightgray")
title_label.pack(pady=(10,5))

# input field
entry = tk.Entry(root, width=18, font=('Arial', 28))
entry.pack(pady=(10,5))

# history box
history = tk.Text(root, height=8, width=55, font=('Arial', 12))
history.pack()
history.insert(tk.END, "History:\n")
history.config(state=tk.DISABLED)

# frame for buttons
btn_frame = tk.Frame(root, bg="lightgray")
btn_frame.pack(pady=20)

def click(txt):
    s = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, s + txt)

def clear():
    entry.delete(0, tk.END)

def calc():
    try:
        expr = entry.get()
        res = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(0, str(res))
        history.config(state=tk.NORMAL)
        history.insert(tk.END, f"{expr} = {res}\n")
        history.config(state=tk.DISABLED)
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# button layout
buttons = [
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+'],
    ['C','(',')','√'],
    ['sin','cos','tan','log'],
    ['exp','pi']
]

# hover effect
def on_enter(e):
    e.widget['bg'] = "#a9a9a9"

def on_leave(e, original_color):
    e.widget['bg'] = original_color

# create buttons
for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        # button colors
        if char in '0123456789.':
            color = "#e0e0e0"  # numbers
        else:
            color = "#f0a500"  # functions

        if char == '=':
            b = tk.Button(btn_frame, text='=', width=5, height=2, bg="#4CAF50", fg="white", command=calc)
        elif char == 'C':
            b = tk.Button(btn_frame, text='C', width=5, height=2, bg="#f44336", fg="white", command=clear)
        elif char == '√':
            b = tk.Button(btn_frame, text='√', width=5, height=2, bg=color, command=lambda: click("math.sqrt("))
        elif char == 'sin':
            b = tk.Button(btn_frame, text='sin', width=5, height=2, bg=color, command=lambda: click("math.sin(math.radians("))
        elif char == 'cos':
            b = tk.Button(btn_frame, text='cos', width=5, height=2, bg=color, command=lambda: click("math.cos(math.radians("))
        elif char == 'tan':
            b = tk.Button(btn_frame, text='tan', width=5, height=2, bg=color, command=lambda: click("math.tan(math.radians("))
        elif char == 'log':
            b = tk.Button(btn_frame, text='log', width=5, height=2, bg=color, command=lambda: click("math.log10("))
        elif char == 'exp':
            b = tk.Button(btn_frame, text='exp', width=5, height=2, bg=color, command=lambda: click("math.exp("))
        elif char == 'pi':
            b = tk.Button(btn_frame, text='π', width=5, height=2, bg=color, command=lambda: click(str(math.pi)))
        else:
            b = tk.Button(btn_frame, text=char, width=5, height=2, bg=color, command=lambda txt=char: click(txt))

        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", lambda e, col=color: on_leave(e, col))
        b.grid(row=r, column=c, padx=5, pady=5)

root.mainloop()
