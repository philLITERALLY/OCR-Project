 # import packages
import cv2

# import my modules
import sort_contours
import config

# init camera
def main(frame):
    # get cropped image
    original = frame[config.cropHeightStart:config.cropHeightEnd, 0:config.cropWidth]

    # apply threshold
    (thresh, edited) = cv2.threshold(original, config.threshLimit, 255, cv2.THRESH_BINARY_INV)

    # WHAT DOES THIS DO?!
    edited = cv2.inRange(edited, 0, 255)

    # calculate amount of white in current frame
    whitePercent = float(cv2.countNonZero(edited)) / float(config.cropArea) * 100.0

    # if white % is greater than set limit give error
    if whitePercent > config.whiteThresh :
        return original, None, []

    # run canny edge detector on image
    edited = cv2.Canny(edited, config.cannyMin, config.cannyMax)

    # run opencv find contours, only external boxes
    (contours, _) = cv2.findContours(edited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # only return contours larger in area than 450
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 450]

    # run contour sort method
    if len(contours) > 0 :
        contours = sort_contours.main(contours)

    # return un-edited image and contours
    return original, edited, contours
