# import packages
import cv2
import numpy as np
import sys

# import my modules
import config

# init camera
def main(char, charCnt) :
    cv2.imshow("Camera", char)
    cv2.moveWindow("Camera", 300, 80)
    
    key = cv2.waitKey(0)

    # quit if '`'
    if key == ord("`") :
        print("Finished Learning")
        sys.exit()
    # skip letter if ' '
    elif key == ord(" ") :
        print("Skipping letter")
    # else store response and image
    else :
        print("Saving letter: " + repr(chr(key%256)) if key%256 < 128 else '?')
        learnKey = np.array(key, np.float32)
        learnKey = np.reshape(learnKey, learnKey.size, 1)
                
        fh = open(config.responsesFile, "ab")
        np.savetxt(fh, learnKey)
        fh.close()

        learnImg = charCnt.copy()
        learnImg = cv2.resize(learnImg, (10, 10))
        learnImg = np.float32(learnImg)
        learnImg = np.reshape(learnImg, (1,100))

        fh = open(config.samplesFile, "ab")
        np.savetxt(fh, learnImg)
        fh.close()

# clear learn
def clear_learn() :
    # clear image
    blankImg = np.zeros((1,1,3), np.uint8)
    cv2.imwrite('/home/pi/OCR-Project/training/train.png', blankImg)

    # clear responses and samples
    open(config.responsesFile, "w").close()
    open(config.samplesFile, "w").close()
