# import packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# import my classes
import config
import camera_setup
import find_contours

# init camera and warmup
(camera, rawCap) = camera_setup.main(config)

#grab
for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port = True) :
        (img, contours) = find_contours.main(config, frame.array)

        num = 1

        for cnt in contours :
                x,y,w,h = cv2.boundingRect(cnt)
                if x > config.edgesGap and (x + w) < (config.camWidth - config.edgesGap) :
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
                    cv2.putText(img, str(num), (x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
                    num = num + 1
        
        cv2.imshow("Frame", img)
        
        key = cv2.waitKey(1) & 0xFF

        rawCap.truncate(0)

        if key == ord("q") :
            break
