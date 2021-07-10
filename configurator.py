import tkinter as tk
from tkinter import filedialog
import os
import csv

root = tk.Tk()
root.title("Configurator")


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
        # if selected == ""
    
    # def unPlace(self):

        

def saveAll():
    game = ["run_game","suspend","resume"]
    with open("config.csv","w") as csv_file:
        csv_file = csv.writer(csv_file)
        for record in records:
            record.cmdWid.save_entry(record.selected.get())
            rec = record.get_record()
            if rec[1] == "Command Type":
                continue
            elif rec[1] == "game":
                for g in game:
                    csv_file.writerow(["",g,rec[2],rec[3],rec[4],""])
            else:
                csv_file.writerow(["",rec[1],rec[2],rec[3],rec[4],""])
          


def new_rec():
    global N
    new_button.grid_remove()
    record = Record(root,N-1)
    record.place_ee()
    records.append(record)
    N+=1
    new_button.grid(row = N, column= 0, columnspan=len(appHead))


appHead = ["sID","Type","Command Reference","Console Message","Voice Command"]

save_button = tk.Button(root,text="Save",command= saveAll)
new_button = tk.Button(root,text="New",command= new_rec)

tk.Label(root,text = appHead[0]).grid(row = 1,column = 0,padx=10)
tk.Label(root,text = appHead[1],width=14).grid(row = 1,column = 1,padx=10)
tk.Label(root,text = appHead[2],width=70).grid(row = 1,column = 2,padx=10)
tk.Label(root,text = appHead[3],width=30).grid(row = 1,column = 3,padx=10)
tk.Label(root,text = appHead[4],width=40).grid(row = 1,column = 4,padx=10)

# root.geometry("1205x480")
N = 3
recordFrame = tk.Frame(root,width=210)
record = Record(root,1)
record.place_ee()
records = []
records.append(record)
save_button.grid(row = 0, column= 0, columnspan=len(appHead))
new_button.grid(row = N, column= 0, columnspan=len(appHead))

with open("config.csv","r") as csv_file:
    csv_file = csv.reader(csv_file)
    for row in csv_file:
        new_rec()
        records[-1]

root.mainloop()
