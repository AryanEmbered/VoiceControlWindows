import tkinter as tk

config_contents = []

# with open("config.csv",'r') as f:
#     for line in f.readlines():
#         if line != '\n':
#             config_contents.append(line.split(',')[1:-1])

root = tk.Tk()
root.geometry("1200x480")
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
        self.optMenu = tk.OptionMenu(root,self.selected,*cmdType)
        self.optMenu.config(width=14)

        
    
    def ref(self,cmdRef = ""):
        self.cmdRef = tk.StringVar(value=cmdRef)
        if self.selected.get() == "openapp" or self.selected.get() == "game":
            self.cmdRefWid = {
                "label":tk.Label(root,text=""),
                "button":tk.button(root,text="Browse Files",command=self.fileBrowser),
                "value":"None"
            }
        else:
            self.cmdRefWid = tk.Entry(root,width=70,bd=3)

    def fileBrowser(self):
        filename = tk.filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("Executables","*.exe*"),("all files","*.*")))
        self.cmdRefWid["Label"].config(text=filename)
        self.cmdRefWid["value"] = filename
    def place(self):
        self.optMenu.grid(row=self.pos,column=0)



appHead = ["Type","Command Reference","Console Message","Voice Command"]

tk.Label(root,text = appHead[0],width=14).grid(row = 0,column = 0,padx=10)
tk.Label(root,text = appHead[1],width=70).grid(row = 0,column = 1,padx=10)
tk.Label(root,text = appHead[2],width=30).grid(row = 0,column = 2,padx=10)
tk.Label(root,text = appHead[3],width=40).grid(row = 0,column = 3,padx=10)

def callback(*args):
    print("Well Hello there")

cmdType = ["openapp", "link", "buttoncomb", "button3comb","keypress","typingshortcut", "game"]
selected = tk.StringVar()
selected.set("opts")
selected.trace_variable("w",callback)
optMenu = tk.OptionMenu(root,selected,*cmdType)
optMenu.config(width=14)
optMenu.grid(row=2,column=0)
cmdRef = tk.StringVar()
e = tk.Entry(root,width=70,bd=3)
e.grid(row=2,column=1)
e1 = tk.Entry(root,width=30,bd=3)
e1.grid(row=2,column=2)
e2 = tk.Entry(root,width=40,bd=3)
e2.grid(row=2,column=3)
root.mainloop()