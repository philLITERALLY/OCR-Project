# import packages
import cv2

# import my modules
import sort_contours
import config

# init camera
def main(frame):
        # get cropped image
        original = frame[config.cropHeightStart:config.cropHeightEnd, 0:config.camWidth]

        # clone original to use for editing
        edited = original

        # run canny edge detector on image
        edited = cv2.Canny(edited, config.cannyLeft, config.cannyRight)

        # run opencv find contours, only external boxes
        (contours, _) = cv2.findContours(edited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # run contour sort method
        if len(contours) > 0 :
                contours = sort_contours.main(contours)

        # return un-edited image and contours
        return original, edited, contours
