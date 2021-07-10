import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import csv

root = tk.Tk()
root.title("Configurator")
root.geometry("1230x480")

rootFrame = tk.Frame(root)
rootFrame.pack(fill=tk.BOTH,expand=1)

canvas = tk.Canvas(rootFrame)
canvas.pack(side = tk.LEFT,fill=tk.BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(rootFrame, orient="vertical", command=canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=my_scrollbar.set)
canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

mainFrame = tk.Frame(canvas)
canvas.create_window((0,0), window=mainFrame, anchor="nw")
# mainFrame.pack()




class CmdWid:
    def __init__(self,frame):
        self.frame = frame
        self.label  = tk.Label(self.frame,text="")
        self.button = tk.Button(self.frame,text="Browse Files",command=self.fileBrowser)
        self.value  = ""
        self.entry = tk.Entry(self.frame,width=70,bd=3)

    def fileBrowser(self):
        filename = filedialog.askopenfilename(initialdir = str(os.getcwd()),
                                        title = "Select a File",
                                        filetypes = (("Executables","*.exe*"),("all files","*.*")))
        self.label.config(text=filename)
        self.value = filename
    
    def place_fb(self):
        self.entry.grid_remove()
        self.label.grid(row=0,column=0)
        self.button.grid(row=0,column=1)
    
    def place_e(self):
        self.label.grid_remove()
        self.button.grid_remove()
        self.entry.grid(row=0,column=0)
    
    def set_label(self,label_text):
        self.label.config(text=label_text)
        self.value = label_text
    
    def set_entry(self,e_text):
        self.entry.insert(0,e_text)
        self.value = e_text

    def save_entry(self,s):
        if s == "game" or s == "openapp":  
            self.value = self.label["text"]
        else:
            self.value = self.entry.get()

class Record:
    def __init__(self,frame,sID):
        self.frame = frame
        self.selected = tk.StringVar()
        cmdType = ["openapp", "link", "buttoncomb", "button3comb","keypress","typingshortcut", "game"]
        self.selected.set("Command Type")
        self.optMenu = tk.OptionMenu(self.frame,self.selected,*cmdType)
        self.optMenu.config(width=14)
        self.sID = sID
        self.sID_Label = tk.Label(self.frame,text=sID)
        self.feedback  = tk.Entry(self.frame,width=30,bd=3)
        self.voiceCMD  = tk.Entry(self.frame,width=40,bd=3)
        self.cmdFrame  = tk.Frame(self.frame,width=70)
        self.cmdWid    = CmdWid(self.cmdFrame)
        self.selected.trace_variable("w",self.place_cmdW)
    
    def place_ee(self):
        self.sID_Label.grid(row=self.sID+1,column=0)
        self.optMenu.grid(row=self.sID+1,column=1)
        self.cmdFrame.grid(row=self.sID+1,column=2)
        self.feedback.grid(row=self.sID+1,column=3)
        self.voiceCMD.grid(row=self.sID+1,column=4)
    
    def place_cmdW(self,*args):
        l = self.selected.get()
        if l == "openapp" or l == "game":
            self.cmdWid.place_fb()
        else:
            self.cmdWid.place_e()
    
    def get_record(self):
        record = [self.sID,self.selected.get(),self.cmdWid.value,self.feedback.get(),self.voiceCMD.get()]
        return record

    def set_record(self,selected,cmd_val,fdbck,voiceCMD):
        self.selected.set(selected)
        # self.cmdWid.value
        if selected == "game" or selected == "openapp":
            self.cmdWid.set_label(cmd_val)
        else:
            self.cmdWid.set_entry(cmd_val)
        self.feedback.insert(0,fdbck)
        self.voiceCMD.insert(0,voiceCMD)


    
    # def unPlace(self):

        

def saveAll():
    game = ["run_game","suspend","resume","destroy"]
    with open("config.csv","w") as csv_file:
        csv_file = csv.writer(csv_file)
        for record in records:
            record.cmdWid.save_entry(record.selected.get())
            rec = record.get_record()
            if rec[1] == "Command Type":
                continue
            elif rec[1] == "game":
                csv_file.writerow(["",game[0],rec[2],rec[3],str("run ")+str(rec[4]),""])
                csv_file.writerow(["",game[0],rec[2],rec[3],str("suspend ")+str(rec[4]),""])
                csv_file.writerow(["",game[0],rec[2],rec[3],str("resume ")+str(rec[4]),""])
                csv_file.writerow(["",game[0],rec[2],rec[3],str("destroy ")+str(rec[4]),""])
            else:
                csv_file.writerow(["",rec[1],rec[2],rec[3],rec[4],""])
          


def new_rec():
    global N
    new_button.grid_remove()
    record = Record(mainFrame,N-1)
    record.place_ee()
    records.append(record)
    N+=1
    new_button.grid(row = N, column= 0, columnspan=len(appHead))


appHead = ["sID","Type","Command Reference","Console Message","Voice Command"]

save_button = tk.Button(mainFrame,text="Save",command= saveAll)
new_button = tk.Button(mainFrame,text="New",command= new_rec)

tk.Label(mainFrame,text = appHead[0]).grid(row = 1,column = 0,padx=10)
tk.Label(mainFrame,text = appHead[1],width=14).grid(row = 1,column = 1,padx=10)
tk.Label(mainFrame,text = appHead[2],width=70).grid(row = 1,column = 2,padx=10)
tk.Label(mainFrame,text = appHead[3],width=30).grid(row = 1,column = 3,padx=10)
tk.Label(mainFrame,text = appHead[4],width=40).grid(row = 1,column = 4,padx=10)

# root.geometry("1205x480")
N = 2
recordFrame = tk.Frame(mainFrame,width=210)
records = []
save_button.grid(row = 0, column= 0, columnspan=len(appHead))
new_button.grid(row = N, column= 0, columnspan=len(appHead))
flag = True
with open("config.csv","r") as csv_file:
    csv_file = csv.reader(csv_file)
    for row in csv_file:
        if row == []:
            continue
        record = row[1:-1]
        if record[0] == "run_game":
            new_rec()
            records[-1].set_record("game",record[1],record[2],record[3])
            flag = False
        elif record[0] in ["suspend","resume","destroy"]:
            continue
        else:
            new_rec()
            flag = False
            records[-1].set_record(*record)
if flag:
    record = Record(mainFrame,1)
    records.append(record)
    record.place_ee()

root.mainloop()
