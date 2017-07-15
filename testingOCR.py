# import packages
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
import learn_ocr

class App(threading.Thread) :
        def __init__(self) :
                threading.Thread.__init__(self)
                self.start()
        def callback(self) :
                self.root.quit()
        def train(self) :
                global learnMode
                if (self.root.trainBtn.cget('text') == "TRAIN") :
                        # Set App to learn mode
                        learnMode = True
                        self.root.headerLbl.configure(text="Learn Mode")
                        self.root.headerLbl.place(relx=.4, rely=.1)

                        # Change trainBtn to stop colour
                        self.root.trainBtn.configure(
                                bg="red",
                                activebackground="red",
                                text="STOP TRAIN"
                        )

                        # Change readBtn to learnCurrent
                        self.root.readBtn.configure(
                                bg="yellow",
                                activebackground="yellow",
                                text="LEARN CURRENT"
                        )

                        # Hide stop button
                        self.root.stopBtn.place_forget()
                elif (self.root.trainBtn.cget('text') == "STOP TRAIN") :
                        # Take App out of learn mode
                        learnMode = False
                        self.root.headerLbl.configure(text="Please select a mode")
                        self.root.headerLbl.place(relx=.35, rely=.1)
                        
                        # Change trainBtn to default colour
                        self.root.trainBtn.configure(
                                bg="yellow",
                                activebackground="yellow",
                                text="TRAIN"
                        )

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
        def read(self) :
                global readMode, learnCurrent, runOutputFile, pipe
                if (self.root.readBtn.cget('text') == "READ") :
                        # Set App to read mode
                        readMode = True
                        self.root.headerLbl.configure(text="Read Mode")
                        self.root.headerLbl.place(relx=.4, rely=.1)

                        # Create run output file
                        runOutputFile = 'output/' + str(datetime.now()) + '.txt'
                        f = open(runOutputFile, "w+")
                        f.close()
                        
                        # Change readBtn to stop colour
                        self.root.readBtn.configure(
                                bg="red",
                                activebackground="red",
                                text="STOP READ"
                        )

                        # Hide stop button and learn button
                        self.root.stopBtn.place_forget()
                        self.root.trainBtn.place_forget()
                elif (self.root.readBtn.cget('text') == "STOP READ") :
                        # Take App out of read mode
                        readMode = False
                        self.root.headerLbl.configure(text="Please select a mode")
                        self.root.headerLbl.place(relx=.35, rely=.1)
                        pipe = []
                        
                        # Change trainBtn to default colour
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
                        
                        # Add trainBtn back
                        self.root.trainBtn = tk.Button(
                                self.root,
                                text="TRAIN",
                                width=10,
                                height=5,
                                command=self.train,
                                bg="yellow",
                                activebackground="yellow"
                        )
                        self.root.trainBtn.place(relx=.1, rely=.3)
                elif (self.root.readBtn.cget('text') == "LEARN CURRENT") :
                        learnCurrent = True
        def stop(self) :
                global stopProgram
                stopProgram = True
                cv2.destroyAllWindows()
                sys.exit()
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
                #self.root.wm_overrideredirect(True)
                #self.root.attributes("-fullscreen", True)

                self.root.headerLbl = tk.Label(
                        self.root,
                        text="Please select a mode",
                        font="Helvetica 16 bold",
                        anchor="center"
                )
                self.root.headerLbl.place(relx=.35, rely=.1)
                        
                self.root.trainBtn = tk.Button(
                        self.root,
                        text="TRAIN",
                        width=10,
                        height=5,
                        command=self.train,
                        bg="yellow",
                        activebackground="yellow"
                )
                self.root.trainBtn.place(relx=.1, rely=.3)
        
                self.root.readBtn = tk.Button(
                        self.root,
                        text="READ",
                        width=10,
                        height=5,
                        command=self.read,
                        bg="green",
                        activebackground="green"
                )
                self.root.readBtn.place(relx=.4, rely=.3)
        
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

                self.root.title("OCR Program")
                self.root.mainloop()

app = App()        

# load OCR training
samples = np.loadtxt(config.samplesFile,np.float32)
responses = np.loadtxt(config.responsesFile,np.float32)
responses = responses.reshape((responses.size,1))
runOutputFile = ''

model = cv2.KNearest()
model.train(samples,responses)

stopProgram = False
readMode = False
learnMode = False
learnCurrent = False

if "--clear_learn" in sys.argv :
        learn_ocr.clear_learn()
        print("Learning Cleared")
        sys.exit()

# init camera and warmup
(stream, rawCap) = camera_setup.main()

pipe = []
firstCharPosition = config.edgesGap
blankCount = 0

#grab frames
for (i, f) in enumerate(stream):
        # get image then find and sort contours
        (original, edited, contours) = find_contours.main(f.array)
        drawImg = original.copy()

        num = 0
        
        if readMode :
                num = len(pipe)
                if len(contours) == 0 :
                        blankCount += 1
                else :
                        blankCount = 0
                                
                for cnt in contours :
                        x,y,w,h = cv2.boundingRect(cnt)
                        if x > config.edgesGap and x < firstCharPosition :
                                char = original.copy()[y:y+h, x:x+w]
                                cv2.imwrite("images/Camera" + str(num) + ".png", char)
                                pipe.append({"key": num + 1 , "OCR": []})
                                num += 1
                                firstCharPosition = x
                                break
                        elif x > config.edgesGap :
                                firstCharPosition = x
                                break

        #for each contour draw a bounding box and order number
        for cnt in contours :
                x,y,w,h = cv2.boundingRect(cnt)
                
                if x > config.edgesGap and (x + w) < (config.camWidth - config.edgesGap) :                        
                        if learnMode & learnCurrent :
                                char = original.copy()[y:y+h, x:x+w]
                                charCnt = edited.copy()[y:y+h, x:x+w]
                                learn_ocr.main(char, charCnt)
                        elif learnMode :
                                cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0),2)                                # get character contour and run OCR
                                charCnt = edited.copy()[y:y+h, x:x+w]
                                charCnt = cv2.resize(charCnt, (10, 10))
                                charCnt = np.float32(charCnt)
                                charCnt = np.reshape(charCnt, (1,100))
                                retval, results, neigh_resp, dists = model.find_nearest(charCnt, k = 1)                                # get text of nearest character
                                string = int((results[0][0]))

                                cv2.putText(drawImg, chr(string%256), (x,y+(h/4*3)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
                        else :
                                # get character contour and run OCR
                                charCnt = edited.copy()[y:y+h, x:x+w]
                                charCnt = cv2.resize(charCnt, (10, 10))
                                charCnt = np.float32(charCnt)
                                charCnt = np.reshape(charCnt, (1,100))
                                retval, results, neigh_resp, dists = model.find_nearest(charCnt, k = 1)

                                # get text of nearest character
                                string = int((results[0][0]))

                                for letter in pipe :
                                        if letter['key'] == num :
                                                letter['OCR'].append(string%256)
                                                modeLetter = Counter(letter['OCR']).most_common(1)[0][0]
                                                #cv2.putText(drawImg, chr(modeLetter), (x,y+(h/4*3)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
                                                cv2.putText(drawImg, str(num), (x,y+(h/4*3)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                                                break

                        num -= 1

        if learnMode & learnCurrent:
                print("Finished learning current screen")
                learnCurrent = False

                # reload OCR training
                samples = np.loadtxt(config.samplesFile,np.float32)
                responses = np.loadtxt(config.responsesFile,np.float32)
                responses = responses.reshape((responses.size,1))

                model = cv2.KNearest()
                model.train(samples,responses)

        # show camera feed
        cv2.imshow("Camera", drawImg)
        
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
        # print full translate
        elif (len(pipe) > 0) & readMode & (blankCount > 10) :
                translate = ""
                stats = []
                for letter in sorted(pipe, key=lambda x: (x['key']), reverse=True) :
                        median = Counter(letter['OCR']).most_common(1)[0][0]
                        stats.append("Letter: " + chr(median) + "  -  Total: " + str(len(letter['OCR'])) + "  -  Mode: " + str(letter['OCR'].count(median) * 100 / len(letter['OCR'])) + "%")
                        translate = translate + str(chr(Counter(letter['OCR']).most_common(1)[0][0]))
                
                fh = open(runOutputFile, "a+")
                fh.write("Output String = " + translate + "\n")
                for letter in stats :
                        fh.write(letter + "\n")
                fh.close()

                pipe = []
                firstCharPosition = config.edgesGap
        elif (key == ord("=")) :
                config.cannyLeft = config.cannyLeft + 10
                print(config.cannyLeft)
                #config.cropHeightEnd = config.cropHeightEnd + 10
                #print config.cropHeightEnd
        elif (key == ord("-")) :
                config.cannyLeft = config.cannyLeft - 10
                print(config.cannyLeft)
                #config.cropHeightEnd = config.cropHeightEnd - 10
                #print config.cropHeightEnd
        elif (key == ord("]")) :
                config.cannyRight = config.cannyRight + 10
                print(config.cannyRight)
                #config.cropHeightStart = config.cropHeightStart + 10
                #print config.cropHeightStart
        elif (key == ord("[")) :
                config.cannyRight = config.cannyRight - 10
                print(config.cannyRight)
                #config.cropHeightStart = config.cropHeightStart - 10
                #print config.cropHeightStart
