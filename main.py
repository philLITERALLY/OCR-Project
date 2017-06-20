# import packages
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from collections import Counter

# import the GUI packages
from Tkinter import *
from PIL import Image
from PIL import ImageTk

# import my classes
import config
import camera_setup
import find_contours
import learn_ocr

# load OCR training
samples = np.loadtxt('training/samples.dat',np.float32)
responses = np.loadtxt('training/responses.dat',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.KNearest()
model.train(samples,responses)

learnMode = False
learnCurrent = False

if "--clear_learn" in sys.argv :
        learn_ocr.clear_learn()
        print("Learning Cleared")
        sys.exit()
elif "--learn" in sys.argv :
        print("Starting learning mode")
        print("Press TAB to learn current screen")
        learnMode = True
elif any(True for arg in config.helpText if arg in sys.argv) :
        config.printHelp()
        sys.exit()
elif "-r" in sys.argv :
        print("Performing OCR")
else :
        print("Please provide an argument. Help listed below.\n")
        config.printHelp()
        sys.exit()

print("Press ` to stop program")

# init camera and warmup
(camera, rawCap) = camera_setup.main()

pipe = []
firstCharPosition = config.edgesGap

#grab frames
for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port = True) :
        # get image then find and sort contours
        (original, edited, contours) = find_contours.main(frame.array)
        drawImg = original.copy()

        num = 0
        
        if not learnMode :
                num = len(pipe)
                for cnt in contours :
                        x,y,w,h = cv2.boundingRect(cnt)
                        if x > config.edgesGap and x < firstCharPosition :
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
                                                cv2.putText(drawImg, chr(modeLetter), (x,y+(h/4*3)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
                                                break

                        num -= 1

        if learnMode & learnCurrent:
                print("Finished learning current screen")
                learnCurrent = False

                # reload OCR training
                samples = np.loadtxt('training/samples.dat',np.float32)
                responses = np.loadtxt('training/responses.dat',np.float32)
                responses = responses.reshape((responses.size,1))

                model = cv2.KNearest()
                model.train(samples,responses)

        # show camera feed
        cv2.imshow("Frame", drawImg)

        # if q key is pressed exit program
        key = cv2.waitKey(1) & 0xFF
        rawCap.truncate(0)
        # if 'q' is pressed stop program
        if key == ord("`") :
                print("Stopping program")
                break
        # if learn mode and 'l' is pressed
        # current screen can be learnt
        elif (key == ord("\t")) & learnMode :
                print("Learning current screen. Enter corresponding characters to shown images.")
                learnCurrent = True
        # print full translate
        elif (key == ord("\n")) :
                translate = ""
                print("Full array trasnlate : ")
                for letter in sorted(pipe, key=lambda x: (x['key']), reverse=True) :
                        median = Counter(letter['OCR']).most_common(1)[0][0]
                        print "Letter: " + chr(median) + "  -  Total: " + str(len(letter['OCR'])) + "  -  Mode: " + str(letter['OCR'].count(median) * 100 / len(letter['OCR'])) + "%"
                        translate = translate + str(chr(Counter(letter['OCR']).most_common(1)[0][0]))
                print translate      
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
