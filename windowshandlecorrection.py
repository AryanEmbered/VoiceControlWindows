import pygetwindow as gw
import win32process
import win32api
import win32con

# print(gw.getAllTitles())

# print(gw.getAllWindows())

print(gw.getWindowsWithTitle('WhatsApp'))

# print("active window", gw.getActiveWindow())

# print("active window title", gw.getActiveWindow().title)

# print("selected handle is =", gw.getWindowsWithTitle('PyGetWindow'))

# app = gw.getWindowsWithTitle('PyG')[0]

# app.maximize()


def processname_from_handle(hwnd):
    pid = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
    proc_name_path = win32process.GetModuleFileNameEx(handle, 0)
    proc_name = proc_name = proc_name_path.rsplit("\\", 1)[1]
    '''print("procname with path", proc_name_path)
    print("procname from handle (removing the path)", proc_name)'''
    return proc_name


def compatibility(input):
    modstring = str(input).replace("[Win32Window(hWnd=", "")
    modstring2 = modstring.replace(")]", "")
    print(modstring2)
    return(modstring2)


print(processname_from_handle(gw.getWindowsWithTitle('WhatsApp')))

processname_from_handle(131942)

def restorewindow(processname):
    windowname = processname.split(".")[0]
    # print("selected handle is =", gw.getWindowsWithTitle(windowname))
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    # print(windowhandle.isMaximized)
    if windowhandle.isMaximized is True:
        windowhandle.activate()
    else:
        windowhandle.maximize()


def minimizewindow(processname):
    windowname = processname.split(".")[0]
    # print("selected handle is =", gw.getWindowsWithTitle(windowname))
    windowhandle = gw.getWindowsWithTitle(windowname)[0]
    # print(windowhandle.isMaximized)
    windowhandle.minimize()


'''minimizewindow("Sekiro.exe")

restorewindow("Sekiro.exe")'''

'''windowtitle_path = gw.getActiveWindow().title
if "\\" in windowtitle_path:
    windowtitle = windowtitle_path.rsplit("\\", 1)[1]
    if ".exe" in windowtitle:
        windowname = windowtitle.replace(".exe", "")
    else:
        windowname = windowtitle
elif ".exe" in windowtitle_path:
    windowtitle_path.replace(".exe", "")
else:
    windowname = windowtitle_path
print(windowname)'''
