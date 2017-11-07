# import packages
# check RAM usage // free -m -s 0.1 //
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from datetime import datetime
import cv2
import numpy as np
from collections import Counter

# import the GUI packages
import Tkinter as tk
import threading
from PIL import Image
from PIL import ImageTk

# import my classes
import config
import camera_setup
import find_contours
import settings_window

if config.automation :
        import automationhat

class App(threading.Thread) :
        def __init__(self) :
                threading.Thread.__init__(self)
                self.start()
        def callback(self) :
                self.root.quit()
        def settings_menu(self, other) :
                window = settings_window.main(self.root)
        def upCrop(self) :
                if config.cropHeightStart + config.cropHeight >= config.camHeight :
                        self.root.cropUpBtn.configure(text="MAX")
                else :
                        config.cropHeightStart += 10
                        config.cropHeightEnd = config.cropHeightStart + config.cropHeight

                if config.cropHeightStart != 0 :
                        self.root.cropDownBtn.configure(text=u"\u2B07")
        def downCrop(self) :
                if config.cropHeightStart - 10 <= 0 :
                        self.root.cropDownBtn.configure(text="MAX")
                else :
                        config.cropHeightStart -= 10
                        config.cropHeightEnd = config.cropHeightStart + config.cropHeight

                if config.cropHeightStart + config.cropHeight != config.camHeight :
                        self.root.cropUpBtn.configure(text=u"\u2B06")
        def read(self) :
                global readMode
                if (self.root.readBtn.cget('text') == "RUN") :
                        # Set App to read mode
                        readMode = True

                        # Change readBtn to stop colour
                        self.root.readBtn.configure(
                                bg="red",
                                activebackground="red",
                                text="PAUSE"
                        )

                elif (self.root.readBtn.cget('text') == "PAUSE") :
                        # Take App out of read mode
                        readMode = False

                        # Change readBtn to default
                        self.root.readBtn.configure(
                                bg="green",
                                activebackground="green",
                                text="RUN"
                        )
        def stop(self) :
                global stopProgram
                stopProgram = True
        def run(self) :
                self.root = tk.Tk()
                self.root.attributes("-fullscreen", True)
                self.root.updateConfig = False
                self.root.shutDown = False

                self.root.headerLbl = tk.Label(
                        self.root,
                        text="LOW COST AUTOMATION",
                        font="Helvetica 16 bold",
                        anchor="center"
                )
                self.root.headerLbl.place(relx=.33, rely=.48)
                self.root.headerLbl.bind("<Button-1>", self.settings_menu)

                self.root.cropUpBtn = tk.Button(
                        self.root,
                        text=u"\u2B06",
                        font="Helvetica 16 bold",
                        width=15,
                        height=2,
                        command=self.upCrop,
                        bg="yellow",
                        activebackground="yellow"
                )
                self.root.cropUpBtn.place(relx=.02, rely=.65)

                self.root.cropDownBtn = tk.Button(
                        self.root,
                        text=u"\u2B07",
                        font="Helvetica 16 bold",
                        width=15,
                        height=2,
                        command=self.downCrop,
                        bg="yellow",
                        activebackground="yellow"
                )
                self.root.cropDownBtn.place(relx=.02, rely=.84)

                self.root.readBtn = tk.Button(
                        self.root,
                        text="RUN",
                        width=50,
                        height=10,
                        command=self.read,
                        bg="green",
                        activebackground="green"
                )
                self.root.readBtn.place(relx=.45, rely=.65)

                image = Image.open("/home/pi/OCR-Project/initialising.png").resize((780, 146))
                cameraScreen = ImageTk.PhotoImage(image)
                self.root.cameraLabel = tk.Label(image=cameraScreen)
                self.root.cameraLabel.place(relx=.01, rely=.01)

                self.root.title("OCR Program")
                self.root.mainloop()

app = App()

stopProgram = False
readMode = False

# init camera and warmup
(stream, rawCap) = camera_setup.main()

emptyStartTime = 0
stuckStrip = False
alarmOn = False
font = cv2.FONT_HERSHEY_SIMPLEX

# try/except statement is a pretty ugly hack to get around
# a RunTime error that Tkinter throws due to threading
try:
        #grab frames
        for (i, f) in enumerate(stream):
                # get cropped image
                croppedFrame = f.array[config.cropHeightStart:config.cropHeightEnd, 0:config.camWidth]
                bandw = Image.fromarray(croppedFrame).convert('1')
                if bandw.getcolors()[0] > bandw.getcolors()[1] :
                        stuckStrip = False
                else :
                        stuckStrip = True

                # get image then find and sort contours
                (original, edited, contours) = find_contours.main(f.array)
                drawImg = original.copy()

                blobCount = 0

                if readMode :
                        #for each contour draw a bounding box and order number
                        if not stuckStrip :
                                for cnt in contours :
                                        x,y,w,h = cv2.boundingRect(cnt)
                                        if x > config.edgesGap and (x + w) < (config.camWidth - config.edgesGap) :
                                                cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0), 2)
                                                blobCount += 1

                        if (blobCount <= config.minBlobCount or stuckStrip) & (emptyStartTime == 0) :
                                emptyStartTime = time.time()
                        elif (blobCount <= config.minBlobCount or stuckStrip) & ((time.time() - emptyStartTime) > config.alarmTime) :
                                alarmOn = True
                                if config.automation :
                                        automationhat.relay.one.on()
                                        automationhat.light.comms.on()
                                else :
                                        cv2.putText(
                                                drawImg,
                                                'ALERT',     # Text
                                                (10, 30),    # Position
                                                font,        # Font
                                                1,           # Size
                                                (255, 0, 0), # Colour
                                                2            # Bold
                                        )
                        elif (blobCount >= (config.minBlobCount + 1) and not stuckStrip) :
                                emptyStartTime = 0
                                if config.automation & alarmOn:
                                        automationhat.relay.one.off()
                                        automationhat.light.comms.off()
                                alarmOn = False
                else :
                        emptyStartTime = 0
                        if config.automation & alarmOn :
                                automationhat.relay.one.off()
                                automationhat.light.comms.off()
                        alarmOn = False

                image = Image.fromarray(drawImg).resize((
                        500 + int(config.cropWidth/float(config.camWidth)*280.0),
                        135 + int(config.cropHeight/float(config.camHeight)*60.0)
                ))
                photo = ImageTk.PhotoImage(image)

                app.root.cameraLabel.configure(image=photo)
                app.root.cameraLabel.image = photo

                if app.root.updateConfig:
                        config = reload(config)
                        if config.automation :
                                import automationhat
                        else :
                                try :
                                        del automationhat
                                except :
                                        print('Nothing imported')
                        app.root.updateConfig = False

                if app.root.shutDown:
                        try:
                            app.root.quit()
                            sys.exit()
                        except Exception as ex:
                            print('Shutdown error')
                            print(ex)

                # if stop is pressed exit program
                key = cv2.waitKey(1) & 0xFF
                # if stop button is pressed stop program
                if stopProgram == True :
                        stream.close()
                        rawCap.close()
                        break

                # clear the stream                
                rawCap.truncate(0)
                rawCap.seek(0)

except Exception as e:
        print('Caught an error')
        print(e)
        stream.close()
        rawCap.close()

app.root.quit()
sys.exit()
