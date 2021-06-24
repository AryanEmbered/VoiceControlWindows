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

SetLogLevel(-1)


def getwordlist():
    wordlist = []
    i = 4
    f = open('config.txt', 'r')
    config = f.read().split('-+-')
    f.close()
    lengthofconfig = len(config)
    while i < lengthofconfig:
        towrite = '"' + config[i] + '"'
        wordlist.append(towrite)
        i = i+5
    wordlist.append('"type", "dictate", "transcribe", "dictation", "voice on", "voice song", "start voice", "mike on", "mic on", "turn on",  "voice of", "close", "mike of", "nike of", "micron", "down", "scroll", "gown", "up", "top", "previous", "application", "done", "tab", "switch application", "suspend","resume", "turn of"')
    words = str(wordlist).replace("'", "")
    return words


MODEL = Model("indian")
rec = KaldiRecognizer(MODEL, 16000, getwordlist())

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


def dictation(l):
    dictation = ["transcribe", "dictate", "dictation"]
    for x in dictation:
        if x in l:
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
    engine.save_to_file(text, 'lastcommand.wav')
    engine.runAndWait()


def openapp(location, command):
    for x in command:
        if x in l:
            subprocess.run([location])
            print(location)
            break


def cmdcommand(location, command):
    for x in command:
        if x in l:
            path = location.rsplit("\\",1)[0]
            os.chdir(path)
            exename = location.rsplit("\\",1)[1]
            os.startfile(exename)
            os.chdir(owd)
            #os.startfile(location)
            '''cmdstring = '"'+location+'"'
            print(cmdstring)
            subprocess.check_output(cmdstring, shell=True)
            subprocess.run([location])
            print(location)'''
            break


def link(link, command):
    for x in command:
        if x in l:
            webbrowser.open(link)
            break


def buttoncomb(but1, but2, command):
    for x in command:
        if x in l:
            pyautogui.hotkey(but1, but2)
            break


def button3comb(but1, but2, but3, command):
    for x in command:
        if x in l:
            pyautogui.hotkey(but1, but2, but3)
            break


def typingshortcut(command, word):
    for x in command:
        if x in l:
            pyautogui.write(word)
            break


def keypress(command, key):
    for x in command:
        if x in l:
            pyautogui.typewrite([key], interval=0)
            break


def suspendapplication(processname):
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    output = str(subprocess.check_output("tasklist", shell=True))
    if processname in output:
        print(processname, " is running")
        cmdstring = 'suspend.exe '+processname
        os.system(cmdstring)
        #speak("process suspended")


def resume(processname):
    cmdstring = cmdstring = 'suspend.exe '+'-r '+processname
    os.system(cmdstring)
    #speak("process resume")


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
    for x in command:
        if x in l:
            print("scrolling now")
            pyautogui.scroll(a)
            break


def main():
    loop = True
    while(loop is True):
        Mic = True
        on(Mic)
        Mic = False
        off(Mic)


def on(Mic):
    global suspended
    suspended = {}
    f = open('config.txt', 'r')
    config = f.read().split('-+-')
    f.close()
    while Mic is True:

        global l
        print("listening")
        l = listen()

        dictation(l)

        if "top" in l:
            upscroll = ["up", "top"]
            scroll(upscroll, 5000)
        if "scroll" in l:
            downscroll = ["down", "scroll", "gown"]
            scroll(downscroll, -600)

        if "previous application" in l:
            alttab()

        if l in config:
            if "openapp" in config[config.index(l)-3]:
                print("Opening app: ", config[config.index(l)-1])
                openapp(config[config.index(l)-2],
                        config[config.index(l)])

            if "cmdcommand" in config[config.index(l)-3]:
                print("Running cmd command: ", config[config.index(l)-1])
                cmdcommand(config[config.index(l)-2],
                           config[config.index(l)])

            if "link" in config[config.index(l)-3]:
                print("Opening Link to ", config[config.index(l)-1])
                link(config[config.index(l)-2],
                     config[config.index(l)])

            if "buttoncomb" in config[config.index(l)-3]:
                print("Button press command: ",
                      config[config.index(l)-1])
                buttoncomb(
                    config[config.index(l)-2].split("+")[0],
                    config[config.index(l)-2].split("+")[1],
                    config[config.index(l)])

            if "button3comb" in config[config.index(l)-3]:
                print("Button press command: ",
                      config[config.index(l)-1])
                button3comb(
                    config[config.index(l)-2].split("+")[0],
                    config[config.index(l)-2].split("+")[1],
                    config[config.index(l)-2].split("+")[2],
                    config[config.index(l)])

            if "keypress" in config[config.index(l)-3]:
                print("single keypress command: ",
                      config[config.index(l)-1])
                keypress(
                    config[config.index(l)],
                    config[config.index(l)-2].split("+")[0])

            if "typingshortcut" in config[config.index(l)-3]:
                print("typecommand command: ",
                      config[config.index(l)-1])
                typingshortcut(
                    config[config.index(l)],
                    config[config.index(l)-2].split("+")[0])

            if "appsuspender" in config[config.index(l)-3]:
                print("Suspend command: ", config[config.index(l)-1])
                suspended[config[config.index(l)-2]] = win32gui.GetForegroundWindow()
                suspendapplication(config[config.index(l)-2])

            if "resume" in config[config.index(l)-3]:
                print("resume command: ", config[config.index(l)-1])
                resume(config[config.index(l)-2])
                key = config[config.index(l)-2]
                win32gui.ShowWindow(suspended.get(key), win32con.SW_SHOWNORMAL)

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
