import tkinter as tk

config_contents = []

with open("config.txt",'r') as f:
    for line in f.readlines():
        if line != '\n':
            config_contents.append(line.split(',')[1:-1])

root = tk.Tk()
root.geometry("800x450")

cmdType = [
    "openapp",
    "link",
    "buttoncomb",
    "button3comb",
    "keypress",
    "typingshortcut",
    "game"
]

selected = tk.StringVar()
selected.set("Command Type")

optMenu = tk.OptionMenu(root,selected,*cmdType)
optMenu.config(width=20)
optMenu.grid(row = 1,column=1)


root.mainloop()
