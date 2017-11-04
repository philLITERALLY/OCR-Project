# import the GUI packages
import sys
import Tkinter as tk

# import my classes
import config

def stopApp(root):
    root.shutDown = True
    window.destroy()

def textReplace(configFileData, field, initial, updated):
    return configFileData.replace(
        '{0} = {1}'.format(field, initial),
        '{0} = {1}'.format(field, updated)
    )

def exitSettings(root):
    with open('/home/pi/OCR-Project/config.py', 'r') as configFile:
        configFileData = configFile.read()

    configFileData = textReplace(configFileData, 'camFrameRate', config.camFrameRate, window.frameTxt.get())
    configFileData = textReplace(configFileData, 'shutterSpeed', config.shutterSpeed, window.shutterTxt.get())
    configFileData = textReplace(configFileData, 'cropWidth', config.cropWidth, window.widthTxt.get())
    configFileData = textReplace(configFileData, 'cropHeight', config.cropHeight, window.heightTxt.get())

    configFileData = textReplace(configFileData, 'automation', config.automation, automation.get())

    configFileData = textReplace(configFileData, 'cannyMin', config.cannyMin, window.minTxt.get())
    configFileData = textReplace(configFileData, 'cannyMax', config.cannyMax, window.maxTxt.get())
    configFileData = textReplace(configFileData, 'threshLimit', config.threshLimit, window.threshTxt.get())
    configFileData = textReplace(configFileData, 'whiteThresh', config.whiteThresh, window.whiteTxt.get())
    configFileData = textReplace(configFileData, 'alarmTime', config.alarmTime, window.alarmTxt.get())
    configFileData = textReplace(configFileData, 'minBlobCount', config.minBlobCount, window.blobTxt.get())

    with open('/home/pi/OCR-Project/config.py', 'w') as configFile:
        configFile.write(configFileData)

    root.updateConfig = True
    window.destroy()

def resetSettings(root):
    with open('/home/pi/OCR-Project/config_defaults.py', 'r') as configFileDefaults:
        configFileDefaultsData = configFileDefaults.read()
    with open('/home/pi/OCR-Project/config.py', 'w') as configFile:
        configFile.write(configFileDefaultsData)
    root.updateConfig = True
    window.destroy()

def createLabel(text, size, style, window):
    return tk.Label(
            window,
            text=text,
            font="Helvetica {0} {1}".format(size, style),
            anchor="center"
    )

def createBtn(text, width, height, command, colour, window, root):
    return tk.Button(
            window,
            text=text,
            width=width,
            height=height,
            command= lambda: command(root),
            bg=colour,
            activebackground=colour
    )

def createTxt(width, window):
    return tk.Entry(
        window,
        width=width,
    )

def main(root) :
    global window
    window = tk.Toplevel(root)
    window.attributes("-fullscreen", True)
    window.title("Engineer's Menu")

    window.headerLbl = createLabel("ENGINEER'S MENU", 16, 'bold', window)
    window.headerLbl.place(relx=.38, rely=.04)

    window.cameraLbl = createLabel("CAMERA", 8, 'bold', window)
    window.cameraLbl.place(relx=.19, rely=.12)

    window.frameLbl = createLabel("FRAME RATE", 8, '', window)
    window.frameLbl.place(relx=.05, rely=.2)
    window.frameTxt = createTxt(10, window)
    window.frameTxt.insert(0, config.camFrameRate)
    window.frameTxt.place(relx=.28, rely=.19)

    window.shutterLbl = createLabel("SHUTTER SPEED", 8, '', window)
    window.shutterLbl.place(relx=.05, rely=.28)
    window.shutterTxt = createTxt(10, window)
    window.shutterTxt.insert(0, config.shutterSpeed)
    window.shutterTxt.place(relx=.28, rely=.27)

    window.resolutionLbl = createLabel("RESOLUTION", 8, '', window)
    window.resolutionLbl.place(relx=.05, rely=.36)

    window.heightLbl = createLabel("H", 8, '', window)
    window.heightLbl.place(relx=.08, rely=.42)
    window.heightTxt = createTxt(10, window)
    window.heightTxt.insert(0, config.cropHeight)
    window.heightTxt.place(relx=.28, rely=.41)

    window.widthLbl = createLabel("W", 8, '', window)
    window.widthLbl.place(relx=.08, rely=.48)
    window.widthTxt = createTxt(10, window)
    window.widthTxt.insert(0, config.cropWidth)
    window.widthTxt.place(relx=.28, rely=.47)

    window.cameraLbl = createLabel("OTHER", 8, 'bold', window)
    window.cameraLbl.place(relx=.19, rely=.57)

    global automation
    automation = tk.BooleanVar()
    automation.set(config.automation)
    window.alarmLbl = createLabel("AUTOMATION HAT", 8, '', window)
    window.alarmLbl.place(relx=.05, rely=.65)
    window.automationCheck = tk.Checkbutton(window, variable=automation)
    window.automationCheck.place(relx=.27, rely=.64)

    window.cameraLbl = createLabel("OCR", 8, 'bold', window)
    window.cameraLbl.place(relx=.75, rely=.12)

    window.cannyLbl = createLabel("CANNY", 8, '', window)
    window.cannyLbl.place(relx=.61, rely=.2)

    window.minLbl = createLabel("MIN", 8, '', window)
    window.minLbl.place(relx=.64, rely=.26)
    window.minTxt = createTxt(10, window)
    window.minTxt.insert(0, config.cannyMin)
    window.minTxt.place(relx=.84, rely=.25)

    window.maxLbl = createLabel("MAX", 8, '', window)
    window.maxLbl.place(relx=.64, rely=.32)
    window.maxTxt = createTxt(10, window)
    window.maxTxt.insert(0, config.cannyMax)
    window.maxTxt.place(relx=.84, rely=.31)

    window.threshLbl = createLabel("THRESHOLD", 8, '', window)
    window.threshLbl.place(relx=.61, rely=.4)
    window.threshTxt = createTxt(10, window)
    window.threshTxt.insert(0, config.threshLimit)
    window.threshTxt.place(relx=.84, rely=.39)

    window.whiteLbl = createLabel("STUCK TAPE WHITE (%)", 8, '', window)
    window.whiteLbl.place(relx=.61, rely=.48)
    window.whiteTxt = createTxt(10, window)
    window.whiteTxt.insert(0, config.whiteThresh)
    window.whiteTxt.place(relx=.84, rely=.47)

    window.blobLbl = createLabel("MIN BLOB COUNT", 8, '', window)
    window.blobLbl.place(relx=.61, rely=.56)
    window.blobTxt = createTxt(10, window)
    window.blobTxt.insert(0, config.minBlobCount)
    window.blobTxt.place(relx=.84, rely=.55)

    window.alarmLbl = createLabel("ALARM WAIT (SEC)", 8, '', window)
    window.alarmLbl.place(relx=.61, rely=.64)
    window.alarmTxt = createTxt(10, window)
    window.alarmTxt.insert(0, config.alarmTime)
    window.alarmTxt.place(relx=.84, rely=.63)

    window.exitBtn = createBtn("SAVE SETTINGS", 12, 6, exitSettings, 'yellow', window, root)
    window.exitBtn.place(relx=.05, rely=.76)

    window.resetBtn = createBtn("RESET SETTINGS", 12, 6, resetSettings, 'orange', window, root)
    window.resetBtn.place(relx=.425, rely=.76)

    window.shutdownBtn = createBtn("SHUTDOWN", 12, 6, stopApp, 'red', window, root)
    window.shutdownBtn.place(relx=.8, rely=.76)

    return window
