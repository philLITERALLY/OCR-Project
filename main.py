# import packages
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# import my classes
import config
import camera_setup
import find_contours
import learn_ocr

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
(camera, rawCap) = camera_setup.main(config)

#grab frames
for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port = True) :
        # get image then find and sort contours
        (img, contours) = find_contours.main(config, frame.array)
        drawImg = img.copy()

        num = 1

        #for each contour draw a bounding box and order number
        for cnt in contours :
                x,y,w,h = cv2.boundingRect(cnt)
                if x > config.edgesGap and (x + w) < (config.camWidth - config.edgesGap) :
                        if learnMode & learnCurrent :
                                char = img.copy()[y:y+h, x:x+w]
                                learn_ocr.main(char)
                                                        
                        cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0),2)
                        cv2.putText(drawImg, str(num), (x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
                        num = num + 1

        if learnMode & learnCurrent:
                print("Finished learning current screen")
                learnCurrent = False

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
        #current screen can be learnt
        elif (key == ord("\t")) & learnMode :
                print("Learning current screen. Enter corresponding characters to shown images.")
                learnCurrent = True
