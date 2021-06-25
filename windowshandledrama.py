import pygetwindow as gw

print(gw.getAllTitles())

# print(gw.getAllWindows())
# print(gw.getWindowsWithTitle('WhatsApp'))


# print("active window", gw.getActiveWindow())

# print("active window title", gw.getActiveWindow().title)

# print("selected handle is =", gw.getWindowsWithTitle('PyGetWindow'))

# app = gw.getWindowsWithTitle('PyG')[0]

# app.maximize()


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
