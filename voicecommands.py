import subprocess
import pyautogui
import webbrowser
import time
import pyttsx3
import pyaudio
from vosk import KaldiRecognizer
from vosk import Model
from vosk import SetLogLevel
import os
import win32gui, win32con
from collections import defaultdict
import csv

SetLogLevel(-1)

global suspended, config, l

def def_val():
    return "No Command Found"

suspended = {}

config = defaultdict(def_val)
fhead = ["type","location","feedback","command"]
with open('config.csv','r') as f:
    f = csv.DictReader(f)
    for record in f:
        cmd = {}
        for head in fhead:
            cmd[head] = record[head]
        config[record["command"]] = cmd


wordlist = []
for key in config.keys():
    towrite = '"' + key + '"'
    wordlist.append(towrite)

wordlist.append('"type", "dictate", "transcribe", "dictation", "voice on", "voice song", "start voice", "mike on", "mic on", "turn on",  "voice of", "close", "mike of", "nike of", "micron", "down", "scroll", "gown", "up", "top", "previous", "application", "done", "tab", "switch application", "suspend","resume", "turn of"')
words = str(wordlist).replace("'", "")



MODEL = Model("indian")
rec = KaldiRecognizer(MODEL, 16000, words)

P = pyaudio.PyAudio()
stream = P.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        DATA = stream.read(50, exception_on_overflow=False)
        if len(DATA) == 0:
            pass
        try:
            if rec.AcceptWaveform(DATA):
                string = rec.Result().rsplit(":")[-1][2:-3]
                if string != "":
                    print(string)
                    return string
        except:
            print("No input")


def dictation():
    speak("transcribe mode")
    print("dictation mode")
    rec = KaldiRecognizer(MODEL, 16000)
    while True:
        # audioio.speak("ready")
        DATA = stream.read(5000, exception_on_overflow=False)
        if len(DATA) == 0:
            pass
        try:
            if rec.AcceptWaveform(DATA):
                string = rec.Result().rsplit(":")[-1][2:-3]
                if string != "":
                    if "stop typing" in string:
                        speak("dictation complete")
                        print("dictation complete")
                        break
                    print(string)
                    pyautogui.write(string)
                    pyautogui.write(" ")
        except:
            pass
        


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.say(text)
    #engine.save_to_file(text, 'lastcommand.wav')
    engine.runAndWait()


def openapp(location, command):
    subprocess.run([location])
    print(location)


def rungame(location, command):
    path = location.rsplit("\\",1)[0]
    os.chdir(path)
    exename = location.rsplit("\\",1)[1]
    os.startfile(exename)
    os.chdir(owd)


def link(link, command):
    webbrowser.open(link)


def buttoncomb(but1, but2, command):
    pyautogui.hotkey(but1, but2)


def button3comb(but1, but2, but3, command):
    pyautogui.hotkey(but1, but2, but3)


def typingshortcut(word, command):
    pyautogui.write(word)


def keypress(key, command):
    pyautogui.typewrite([key], interval=0)


def suspendapplication(processname):
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    output = str(subprocess.check_output("tasklist", shell=True))
    if processname in output:
        print(processname, " is running")
        cmdstring = 'suspend.exe '+processname
        os.system(cmdstring)
        speak("process suspended")
        win_handle_suspended_app = win32gui.GetForegroundWindow()
        suspended[processname] = win_handle_suspended_app


def resume(processname):
    cmdstring = cmdstring = 'suspend.exe '+'-r '+processname
    os.system(cmdstring)
    speak("process resume")
    wintomaximize = suspended.get(processname)
    win32gui.ShowWindow(wintomaximize, win32con.SW_SHOWNORMAL)


def altdoubletab():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.press('tab')
    pyautogui.keyUp('alt')


def alttab():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')


def scroll(command, a):
    print("scrolling now")
    pyautogui.scroll(a)


def main():
    loop = True
    while(loop is True):
        Mic = True
        on(Mic)
        Mic = False
        off(Mic)


def on(Mic):
    while Mic is True:
        global l
        print("listening")
        l = listen()
        dic = ["transcribe", "dictate", "dictation"]
        if l in dic:#
            dictation()
            continue

        if "top" in l:
            upscroll = ["up", "top"]
            scroll(upscroll, 5000)
            continue
        if "scroll" in l:
            downscroll = ["down", "scroll", "gown"]
            scroll(downscroll, -600)
            continue

        if "previous application" in l:
            alttab()
            continue
        if "previous previous application" in l:
            altdoubletab()
            continue
        
        cmd_details = config.get(l)
        print(cmd_details)

        if cmd_details == "No Command Found":
            print(cmd_details)
            continue
        
        
        

        if "openapp" in cmd_details["type"]:
            print("Opening app: ", cmd_details["feedback"])
            openapp(cmd_details["location"],
                    cmd_details["command"])

        if "rungame" in cmd_details["type"]:
            print("Running cmd command: ", cmd_details["feedback"])
            rungame(cmd_details["location"],
                    cmd_details["command"])

        if "link" in cmd_details["type"]:
            print("Opening Link to ", cmd_details["feedback"])
            link(cmd_details["location"],
                    cmd_details["command"])

        if "buttoncomb" in cmd_details["type"]:
            print("Button press command: ",
                    cmd_details["feedback"])
            buttoncomb(
                cmd_details["location"].split("+")[0],
                cmd_details["location"].split("+")[1],
                cmd_details["command"])

        if "button3comb" in cmd_details["type"]:
            print("Button press command: ",
                    cmd_details["feedback"])
            button3comb(
                cmd_details["location"].split("+")[0],
                cmd_details["location"].split("+")[1],
                cmd_details["location"].split("+")[2],
                cmd_details["command"])

        if "keypress" in cmd_details["type"]:
            print("single keypress command: ",
                    cmd_details["feedback"])
            keypress(cmd_details["location"].split("+")[0], cmd_details["command"])

        if "typingshortcut" in cmd_details["type"]:
            print("typecommand command: ",
                    cmd_details["feedback"])
            typingshortcut(cmd_details["location"].split("+")[0], cmd_details["command"])

        if "appsuspender" in cmd_details["type"]:
            print("Suspend command: ", cmd_details["feedback"])
            suspendapplication(cmd_details["location"])

        if "resume" in cmd_details["type"]:
            print("resume command: ", cmd_details["feedback"])
            resume(cmd_details["location"])

        # stopping voice commands
        close = ["voice of", "turn of"]
        for x in close:
            if x in l:
                Mic = False
                print("Program Paused. Speech Recognition turned off")
                break


def off(Mic):
    speak("off")
    print("paused")
    while(Mic is False):
        # audioio.dictation(l)
        b = listen()
        start = ["voice on", "voice song", "start voice", "mike on", "mic on", "turn on", "micron"]
        for x in start:
            if b == x:
                print("Turning on")
                print("Recognised:", b)
                print("Keyword match :", x)
                Mic = True
                speak("on")
                print("resumed listening")
                break



owd = os.getcwd()

Mic = True
if __name__ == "__main__":
    main()
