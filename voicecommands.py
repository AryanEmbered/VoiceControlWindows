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
import win32api
import win32process
import win32con
import win32gui

SetLogLevel(-1)

global suspended, config, input
suspended = []

f = open('config.csv', 'r')
config = f.read().split(',')
f.close()

owd = os.getcwd()


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
    wordlist.append('"maximize", "minimize", "this", "foreground"')
    wordlist.append('"one", "two", "three", "four", "five", "six"')
    wordlist.append('"alpha","beta","gamma","delta"')


    # print("wordlist so far is :", wordlist, "\n")
    words = str(wordlist).replace("'", "")
    return words


words = getwordlist(config)

# print("\nThese are all the recognized voice commands", getwordlist(config))
MODEL = Model("indian")
rec = KaldiRecognizer(MODEL, 16000, words)

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


def process_path(hwnd):
    pid = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
    proc_name = win32process.GetModuleFileNameEx(handle, 0)
    return proc_name


def processname_from_handle(hwnd):
    pid = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
    proc_name_path = win32process.GetModuleFileNameEx(handle, 0)
    proc_name = proc_name = proc_name_path.rsplit("\\", 1)[1]
    '''print("procname with path", proc_name_path)
    print("procname from handle (removing the path)", proc_name)'''
    return proc_name


def get_hwnds_for_pid(pid):
    # untested
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def processname_from_pid(pid):
    cmdstring1 = "tasklist /fi "
    cmdstring2 = "pid eq "
    cmdstring3 = pid
    cmdstring = cmdstring1 + cmdstring2 + str(cmdstring3)
    print(cmdstring)
    output = str(subprocess.check_output(cmdstring, shell=True))
    print(output)


def maximize(handle=""):
    try:
        win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
    except Exception:
        try:
            processname = handle
            windowname = processname.split(".")[0]
            windowtomaximize = gw.getWindowsWithTitle(windowname)[0]
            windowtomaximize.maximize()
        except Exception:
            try:
                time.sleep(1)
                hwnd = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            except Exception:
                print("this application sucks. doesn't even minimize properly.")


def minimize(handle=""):
    try:
        #time.sleep(2)
        win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
    except Exception:
        try:
            processname = handle
            windowname = processname.split(".")[0]
            windowtominimize = gw.getWindowsWithTitle(windowname)[0]
            windowtominimize.minimize()
        except Exception:
            try:
                time.sleep(1)
                hwnd = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            except Exception:
                print("this application sucks Doesn't even minimize properly.")


def destroy(applicationtitle):
    windowname = applicationtitle.split(".")[0]
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    print(windowhandle)
    windowhandle.close()


def suspendapplication(processname):
    output = str(subprocess.check_output("tasklist", shell=True))
    if processname in output:
        cmdstring = 'suspend.exe '+processname
        os.system(cmdstring)
    else:
        print(processname, " is not running")


def resume(processname):
    output = str(subprocess.check_output("tasklist", shell=True))
    if processname in output:
        cmdstring = 'suspend.exe '+'-r '+processname
        os.system(cmdstring)
    else:
        print(processname, " is not suspended")


def updatesuspendedlistfile(string1, string2):
    a_file = open("suspendedprocesses.txt", "r")
    lines = a_file.readlines()
    a_file.close()
    string = lines[0]
    modstring = string.replace(string1, string2)
    new_file = open("suspendedprocesses.txt", "w+")
    for line in lines:
        new_file.write(modstring)
        new_file.close()


def suspendforeground():
    if input == "suspend alpha":
        handle = win32gui.GetForegroundWindow()
        fprocess = processname_from_handle(handle)
        minimize(handle)
        suspendapplication(fprocess)
        slot1 = fprocess + "-" + str(handle)
        updatesuspendedlistfile("alpha", slot1)
    if input == "suspend beta":
        handle = win32gui.GetForegroundWindow()
        fprocess = processname_from_handle(handle)
        minimize(handle)
        suspendapplication(fprocess)
        slot2 = fprocess + "-" + str(handle)
        updatesuspendedlistfile("beta", slot2)
    if input == "suspend gamma":
        handle = win32gui.GetForegroundWindow()
        fprocess = processname_from_handle(handle)
        minimize(handle)
        suspendapplication(fprocess)
        slot3 = fprocess + "-" + str(handle)
        updatesuspendedlistfile("gamma", slot3)
    if input == "suspend delta":
        handle = win32gui.GetForegroundWindow()
        fprocess = processname_from_handle(handle)
        minimize(handle)
        suspendapplication(fprocess)
        slot4 = fprocess + "-" + str(handle)
        print(slot4)
        updatesuspendedlistfile("delta", slot4)



def resumeforeground():
    f = open("suspendedprocesses.txt", "r")
    suspendedstring = f.read()
    suspended = suspendedstring.split(",")
    f.close()

    if input == "resume alpha":
        fprocess_handle = suspended[0]
        fprocess = fprocess_handle.split("-")[0]
        handle = fprocess_handle.split("-")[1]
        resume(fprocess)
        maximize(fprocess)
        updatesuspendedlistfile(suspended[0], "alpha")

    if input == "resume beta":
        fprocess_handle = suspended[1]
        fprocess = fprocess_handle.split("-")[0]
        handle = fprocess_handle.split("-")[1]
        resume(fprocess)
        maximize(fprocess)
        updatesuspendedlistfile(suspended[1], "beta")

    if input == "resume gamma":
        fprocess_handle = suspended[2]
        fprocess = fprocess_handle.split("-")[0]
        handle = fprocess_handle.split("-")[1]
        resume(fprocess)
        maximize(fprocess)
        updatesuspendedlistfile(suspended[2], "gamma")

    if input == "resume delta":
        fprocess_handle = suspended[3]
        print(fprocess_handle)
        fprocess = fprocess_handle.split("-")[0]
        print(fprocess)
        handle = fprocess_handle.split("-")[1]
        print(handle)
        resume(fprocess)
        maximize(fprocess)
        updatesuspendedlistfile(suspended[3], "delta")


def inbuiltfunctions():
    dictation(input)
    if "top" in input:
        pyautogui.scroll(5000)
    if "scroll" in input:
        pyautogui.scroll(-600)
    if "previous application" in input:
        pyautogui.keyDown('alt')
        time.sleep(.2)
        pyautogui.press('tab')
        time.sleep(.2)
        pyautogui.keyUp('alt')
    if "previous previous application" in input:
        pyautogui.keyDown('alt')
        time.sleep(.2)
        pyautogui.press('tab')
        time.sleep(.2)
        pyautogui.press('tab')
        pyautogui.keyUp('alt')
    if input == "maximize":
        maximize()
    if input == "minimize":
        minimize()
    suspendforeground()
    resumeforeground()


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

        inbuiltfunctions()

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
                webbrowser.open(commandreference)

            if "buttoncomb" in typeofcommand:
                print("Button press command: ", consoleoutput)
                pyautogui.hotkey(commandreference.split("+")[0],
                                 commandreference.split("+")[1])

            if "button3comb" in typeofcommand:
                print("Button press command: ", consoleoutput)
                pyautogui.hotkey(commandreference.split("+")[0],
                                 commandreference.split("+")[1],
                                 commandreference.split("+")[2])

            if "keypress" in typeofcommand:
                print("single keypress command: ", consoleoutput)
                pyautogui.typewrite([commandreference.split("+")[0]],
                                    interval=0)

            if "typingshortcut" in typeofcommand:
                print("typecommand command: ", consoleoutput)
                pyautogui.write(commandreference.split("+")[0])

            if "appsuspender" in typeofcommand:
                print("Suspend command: ", consoleoutput)
                minimize(commandreference)
                suspendapplication(commandreference)

            if "resume" in typeofcommand:
                print("resume command: ", consoleoutput)
                resume(commandreference)
                maximize(commandreference)

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


f = open("suspendedprocesses.txt", "r")
suspendedstring = f.read()
suspended = suspendedstring.split(",")
f.close()
print("suspended processes are: ", suspended)

Mic = True
if __name__ == "__main__":
    main()
