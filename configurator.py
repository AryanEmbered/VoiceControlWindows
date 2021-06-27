import tkinter as tk

config_contents = []

with open("config.txt",'r') as f:
    for line in f.readlines():
        if line != '\n':
            config_contents.append(line.split(',')[1:-1])

root = tk.Tk()
root.geometry("1100x480")
root.resizable(0,1)
class Record:
    def __init__(self,pos,optS = "Command Type"):
        cmdType = [
            "openapp",
            "link",
            "buttoncomb",
            "button3comb",
            "keypress",
            "typingshortcut",
            "game"
        ]
        self.pos = pos
        self.selected = tk.StringVar(value=optS)
        self.optMenu = tk.OptionMenu(root,self.selected,*cmdType,width = 20)

    
    def ref(self,cmdRef = ""):
        self.cmdRef = tk.StringVar(value=cmdRef)
        if self.selected.get() == "openapp" or self.selected.get() == "game":
            self.cmdRefWid = {
                "label":tk.Label(root,text=""),
                "button":tk.button(root,text="Browse Files",command=self.fileBrowser),
                "value":"None"
            }

    def fileBrowser(self):
        filename = tk.filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("Executables","*.exe*"),("all files","*.*")))
        self.cmdRefWid["Label"].config(text=filename)
        self.cmdRefWid["value"] = filename


appHead = ["Type","Command Reference","Console Message","Voice Command"]

for i in range(4):
    tk.Label(root,text = appHead[i]).grid(row = 1,column = i)

cmdType = ["openapp", "link", "buttoncomb", "button3comb","keypress","typingshortcut", "game"]
selected = tk.StringVar()
selected.set("opts")

optMenu = tk.OptionMenu(root,selected,*cmdType)
optMenu.config(width=14)
optMenu.grid(row=2,column=0,padx=10)
cmdRef = tk.StringVar()
e = tk.Entry(root,width=70,bd=3)
e.grid(row=2,column=1,padx=10)
e1 = tk.Entry(root,width=30,bd=3)
e1.grid(row=2,column=2,padx=10)
e2 = tk.Entry(root,width=40,bd=3)
e2.grid(row=2,column=3,padx=10)
root.mainloop()
