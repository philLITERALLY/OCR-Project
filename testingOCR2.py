# import packages
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from datetime import datetime
import cv2
import numpy as np
from collections import Counter
import automationhat

# import the GUI packages
import Tkinter as tk
import threading
from PIL import Image
from PIL import ImageTk

# import my classes
import config
import camera_setup
import find_contours

class App(threading.Thread) :
        def __init__(self) :
                threading.Thread.__init__(self)
                self.start()
        def callback(self) :
                self.root.quit()
        def read(self) :
                global readMode
                if (self.root.readBtn.cget('text') == "READ") :
                        # Set App to read mode
                        readMode = True
                        self.root.headerLbl.configure(text="Read Mode")
                        self.root.headerLbl.place(relx=.4, rely=.1)
                        
                        # Change readBtn to stop colour
                        self.root.readBtn.configure(
                                bg="red",
                                activebackground="red",
                                text="STOP READ"
                        )

                        # Hide stop button and learn button
                        self.root.stopBtn.place_forget()
                elif (self.root.readBtn.cget('text') == "STOP READ") :
                        # Take App out of read mode
                        readMode = False
                        self.root.headerLbl.configure(text="Please select a mode")
                        self.root.headerLbl.place(relx=.35, rely=.1)

                        # Change readBtn to default
                        self.root.readBtn.configure(
                                bg="green",
                                activebackground="green",
                                text="READ"
                        )
                        
                        # Add stopBtn back
                        self.root.stopBtn = tk.Button(
                                self.root,
                                text="STOP",
                                width=10,
                                height=5,
                                command=self.stop,
                                bg="red",
                                activebackground="red"
                        )
                        self.root.stopBtn.place(relx=.7, rely=.3)
        def stop(self) :
                global stopProgram
                stopProgram = True
                cv2.destroyAllWindows()
                sys.exit()
        def setEmptyThresh(self) :
                global emptyThresh
                emptyThresh = int(self.root.emptyBox.get())
        def setCannyLeftMinus(self) :
                config.cannyLeft -= 10
                self.root.cannyLeftBox.delete(0, len(self.root.cannyLeftBox.get()))
                self.root.cannyLeftBox.insert(0, config.cannyLeft)
        def setCannyLeftPlus(self) :
                config.cannyLeft += 10
                self.root.cannyLeftBox.delete(0, len(self.root.cannyLeftBox.get()))
                self.root.cannyLeftBox.insert(0, config.cannyLeft)
        def setCannyRightMinus(self) :
                config.cannyRight -= 10
                self.root.cannyRightBox.delete(0, len(self.root.cannyRightBox.get()))
                self.root.cannyRightBox.insert(0, config.cannyRight)
        def setCannyRightPlus(self) :
                config.cannyRight += 10
                self.root.cannyRightBox.delete(0, len(self.root.cannyRightBox.get()))
                self.root.cannyRightBox.insert(0, config.cannyRight)
        def run(self) :
                self.root = tk.Tk()
                self.root.protocol("WM_DELETE_WINDOW", self.callback)
                w = self.root.winfo_screenwidth()
                h = int(self.root.winfo_screenheight() / 2.5)
                ws = self.root.winfo_screenwidth()
                hs = self.root.winfo_screenheight()
                x = (ws/2) - (w/2)
                y = hs - h
                self.root.minsize(width=w, height=h)
                self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

                self.root.headerLbl = tk.Label(
                        self.root,
                        text="Please select a mode",
                        font="Helvetica 16 bold",
                        anchor="center"
                )
                self.root.headerLbl.place(relx=.35, rely=.08)

                self.root.emptyLbl = tk.Label(
                        self.root,
                        text="Empty threshold (secs)",
                        font="Helvetica 8",
                        anchor="center"
                )
                self.root.emptyLbl.place(relx=.33, rely=.3)
        
                self.root.emptyBox = tk.Entry(
                        self.root,
                        width=4,
                )
                self.root.emptyBox.insert(0, "20")
                self.root.emptyBox.place(relx=.5, rely=.29)
        
                self.root.emptyBtn = tk.Button(
                        self.root,
                        text="SET",
                        width=2,
                        height=1,
                        command=self.setEmptyThresh,
                )
                self.root.emptyBtn.place(relx=.58, rely=.27)

                self.root.cannyLeftLbl = tk.Label(
                        self.root,
                        text="Canny Left",
                        font="Helvetica 8 bold",
                        anchor="center"
                )
                self.root.cannyLeftLbl.place(relx=.35, rely=.45)
        
                self.root.cannyLeftBox = tk.Entry(
                        self.root,
                        width=4,
                )
                self.root.cannyLeftBox.insert(0, config.cannyLeft)
                self.root.cannyLeftBox.place(relx=.36, rely=.55)
        
                self.root.cannyLeftMinusBtn = tk.Button(
                        self.root,
                        text="-",
                        width=1,
                        height=1,
                        command=self.setCannyLeftMinus,
                )
                self.root.cannyLeftMinusBtn.place(relx=.33, rely=.68)
        
                self.root.cannyLeftPlusBtn = tk.Button(
                        self.root,
                        text="+",
                        width=1,
                        height=1,
                        command=self.setCannyLeftPlus,
                )
                self.root.cannyLeftPlusBtn.place(relx=.39, rely=.68)

                self.root.cannyRightLbl = tk.Label(
                        self.root,
                        text="Canny Right",
                        font="Helvetica 8 bold",
                        anchor="center"
                )
                self.root.cannyRightLbl.place(relx=.55, rely=.45)
        
                self.root.cannyRightBox = tk.Entry(
                        self.root,
                        width=4,
                )
                self.root.cannyRightBox.insert(0, config.cannyRight)
                self.root.cannyRightBox.place(relx=.56, rely=.55)
        
                self.root.cannyRightMinusBtn = tk.Button(
                        self.root,
                        text="-",
                        width=1,
                        height=1,
                        command=self.setCannyRightMinus,
                )
                self.root.cannyRightMinusBtn.place(relx=.53, rely=.68)
        
                self.root.cannyRightPlusBtn = tk.Button(
                        self.root,
                        text="+",
                        width=1,
                        height=1,
                        command=self.setCannyRightPlus,
                )
                self.root.cannyRightPlusBtn.place(relx=.59, rely=.68)
        
                self.root.readBtn = tk.Button(
                        self.root,
                        text="READ",
                        width=10,
                        height=5,
                        command=self.read,
                        bg="green",
                        activebackground="green"
                )
                self.root.readBtn.place(relx=.1, rely=.3)
        
                self.root.stopBtn = tk.Button(
                        self.root,
                        text="STOP",
                        width=10,
                        height=5,
                        command=self.stop,
                        bg="red",
                        activebackground="red"
                )
                self.root.stopBtn.place(relx=.75, rely=.3)

                self.root.title("OCR Program")
                self.root.mainloop()

app = App()        

stopProgram = False
readMode = False

# init camera and warmup
(stream, rawCap) = camera_setup.main()

emptyStartTime = 0
triggerTime = 0
emptyThresh = 20

#grab frames
for (i, f) in enumerate(stream):
        # get image then find and sort contours
        (original, edited, contours) = find_contours.main(f.array)
        drawImg = original.copy()

        blobCount = 0

        if readMode :        
                #for each contour draw a bounding box and order number
                for cnt in contours :
                        x,y,w,h = cv2.boundingRect(cnt)
                        if x > config.edgesGap and (x + w) < (config.camWidth - config.edgesGap) :
                                cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0),2)
                                blobCount += 1

                if (blobCount <= 2) & (emptyStartTime == 0) :
                        emptyStartTime = time.time()
                        triggerTime = 0
                elif (blobCount <= 2) & ((time.time() - emptyStartTime) > emptyThresh) :
                        blankTime = int(round(time.time() - emptyStartTime))
                        if triggerTime == 0 :
                                automationhat.relay.one.toggle()
                                triggerTime = blankTime
                        elif (triggerTime + 1) == blankTime :
                                automationhat.relay.one.toggle()
                                triggerTime = blankTime
                elif (blobCount >= 3) :
                        emptyStartTime = 0
                        triggerTime = 0
        else :
                emptyStartTime = 0
                triggerTime = 0
                

        # show camera feed
        cv2.imshow("Camera", drawImg)
        cv2.moveWindow("Camera", 0, 80)
        
        # if q key is pressed exit program
        key = cv2.waitKey(1) & 0xFF
        rawCap.truncate(0)
        # if stop button is pressed stop program
        if stopProgram == True :                
                # do a bit of cleanup
                cv2.destroyAllWindows()
                stream.close()
                rawCap.close()
                break
