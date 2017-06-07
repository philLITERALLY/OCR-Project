# import packages
import cv2
import numpy as np
import sys

# init camera
def main(char) :
    cv2.imshow("Frame", char)
    
    # if q key is pressed exit program
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

        trainImg = cv2.imread('training/train.png')

        h1, w1 = trainImg.shape[:2]
        h2, w2 = char.shape[:2]
        vis = np.zeros((max(h1, h2), w1+w2, 3), np.uint8)
        vis[:h1, :w1] = trainImg
        vis[:h2, w1:w1+w2] = char
        vis = cv2.cvtColor(vis, cv2.COLOR_BGRA2BGR)

        cv2.imwrite('training/train.png', vis)

        fh = open("training/responses.dat", "a")
        fh.write(str(key) + "\n")
        fh.close()

        fh = open("training/samples.dat", "ab")
        fh.write(str(char))
        fh.write("\n")
        fh.close()

# clear learn
def clear_learn() :
    # clear image
    blankImg = np.zeros((1,1,3), np.uint8)
    cv2.imwrite('training/train.png', blankImg)

    # clear responses and samples
    open("training/responses.dat", "w").close()
    open("training/samples.dat", "w").close()
