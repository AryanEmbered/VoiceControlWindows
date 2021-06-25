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
import pygetwindow as gw

global suspended, config, input
suspended = {}
SetLogLevel(-1)
f = open('config.csv', 'r')
config = f.read().split(',')
f.close()


def getwordlist(config):
    wordlist = []
    i = 4
    lengthofconfig = len(config)
    while i < lengthofconfig:
        towrite = '"' + config[i] + '"'
        wordlist.append(towrite)
        i = i+5
    wordlist.append('"type", "dictate", "transcribe", "dictation", "voice on"')
    wordlist.append('"voice song", "start voice", "mike on", "mic on"')
    wordlist.append('"voice of", "close", "mike of", "nike of", "micron"')
    wordlist.append('"scroll", "gown", "up", "top", "previous", "application"')
    wordlist.append('"tab", "switch application", "suspend","resume"')
    wordlist.append('"done", "turn of", "down", "turn on", "what", "restore"')
    # print("wordlist so far is :", wordlist, "\n")
    words = str(wordlist).replace("'", "")
    return words


# print("\nThese are all the recognized voice commands", getwordlist(config))
MODEL = Model("indian")
rec = KaldiRecognizer(MODEL, 16000, getwordlist(config))

P = pyaudio.PyAudio()
stream = P.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                frames_per_buffer=8000)
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
        except Exception:
            print("No input")


def dictation(input):
    dictation = ["transcribe", "dictate", "dictation"]
    for x in dictation:
        if x in input:
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
                except Exception:
                    pass


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.say(text)
    # engine.save_to_file(text, 'lastcommand.wav')
    engine.runAndWait()


def openapp(location, command):
    path = location.rsplit("\\", 1)[0]
    os.chdir(path)
    exename = location.rsplit("\\", 1)[1]
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


def restorewindow(processname):
    windowname = processname.split(".")[0]
    # print("selected handle is =", gw.getWindowsWithTitle(windowname))
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    # print(windowhandle.isMaximized)
    if windowhandle.isMaximized is True:
        windowhandle.activate()
    else:
        windowhandle.maximize()
        windowhandle.activate()


def minimizewindow(processname):
    windowname = processname.split(".")[0]
    # print("selected handle is =", gw.getWindowsWithTitle(windowname))
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    # print(windowhandle.isMaximized)
    windowhandle.minimize()


def suspendapplication(processname):
    minimizewindow(processname)
    output = str(subprocess.check_output("tasklist", shell=True))
    if processname in output:
        # print(processname, " is running")
        cmdstring = 'suspend.exe '+processname
        os.system(cmdstring)
        # speak("process suspended")
        '''win_handle_suspended_app = win32gui.GetForegroundWindow()
        suspended[processname] = win_handle_suspended_app'''


def destroy(applicationtitle):
    windowname = applicationtitle.split(".")[0]
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    print(windowhandle)
    windowhandle.close()


def resume(processname):
    cmdstring = 'suspend.exe '+'-r '+processname
    os.system(cmdstring)
    # speak("process resume")
    restorewindow(processname)
    '''wintomaximize = suspended.get(processname)
    win32gui.ShowWindow(wintomaximize, win32con.SW_SHOWNORMAL)'''


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


def scrolling():
    if "top" in input:
        upscroll = ["up", "top"]
        scroll(upscroll, 5000)
    if "scroll" in input:
        downscroll = ["down", "scroll", "gown"]
        scroll(downscroll, -600)


def appswitching():
    if "previous application" in input:
        alttab()
    if "previous previous application" in input:
        altdoubletab()


def main():
    loop = True
    while(loop is True):
        Mic = True
        on(Mic)
        Mic = False
        off(Mic)


def on(Mic):
    while Mic is True:
        print("listening")
        global input

        input = listen()

        dictation(input)

        scrolling()

        appswitching()

        if input in config:
            voicecommand = config[config.index(input)]
            consoleoutput = config[config.index(input)-1]
            commandreference = config[config.index(input)-2]
            typeofcommand = config[config.index(input)-3]

            if "destroy" in typeofcommand:
                print("Closing :", consoleoutput)
                destroy(commandreference)

            if "openapp" in typeofcommand:
                print("Opening app: ", consoleoutput)
                openapp(commandreference, voicecommand)

            if "link" in typeofcommand:
                print("Opening Link to ", consoleoutput)
                link(commandreference, voicecommand)

            if "buttoncomb" in typeofcommand:
                print("Button press command: ", consoleoutput)
                buttoncomb(commandreference.split("+")[0],
                           commandreference.split("+")[1], voicecommand)

            if "button3comb" in typeofcommand:
                print("Button press command: ", consoleoutput)
                button3comb(
                    commandreference.split("+")[0],
                    commandreference.split("+")[1],
                    commandreference.split("+")[2], voicecommand)

            if "keypress" in typeofcommand:
                print("single keypress command: ", consoleoutput)
                keypress(commandreference.split("+")[0], voicecommand)

            if "typingshortcut" in typeofcommand:
                print("typecommand command: ", consoleoutput)
                typingshortcut(commandreference.split("+")[0], voicecommand)

            if "appsuspender" in typeofcommand:
                print("Suspend command: ", consoleoutput)
                suspendapplication(commandreference)

            if "resume" in typeofcommand:
                print("resume command: ", consoleoutput)
                resume(commandreference)

        # stopping voice commands
        close = ["voice of", "turn of"]
        for x in close:
            if x in input:
                Mic = False
                print("Program Paused. Speech Recognition turned off")
                break


def off(Mic):
    speak("off")
    print("paused")
    while(Mic is False):
        # audioio.dictation(l)
        b = listen()
        start = ["voice on", "start voice", "mike on", "mic on", "turn on"]
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
