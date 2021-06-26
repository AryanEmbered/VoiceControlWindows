import PySimpleGUI as sg
layout = [
            [sg.Text("Type of command \n choices: openapp, destory, suspend, resume, typingshortcut, buttoncomb, button3comb")],
            [sg.Input()],
            [sg.Text("Comamnd sensitive information\n This field depends on the type of command\n if you want to open application, enter the location/path to the exe,\n to suspend or resume, enter the process name from task manager(go to details page),\n for  button combinations, enter the combination, typingshortcut, type the string ")],
            [sg.Input()],
            [sg.Text("Consoleout of the command \n what you want the command to be called in the console")],
            [sg.Input()],
            [sg.Text("Voicecommand \n what you want to say to trigger the command")],
            [sg.Input()],
            [sg.Button('Start')]
        ]
window = sg.Window('configurator', layout)
event, guivalue = window.read()

type = guivalue[0]
info = guivalue[1]
console = guivalue[2]
voice = guivalue[3]

entry = "\n\n" + "," + type + "," + info + "," + console + "," + voice + ","
print(entry)
f = open("config.csv", "a")
f.write(entry)
f.close()
window.close()
