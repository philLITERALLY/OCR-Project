# import packages
import cv2

# import my classes
import sort_contours

# init camera
def main(config, frame):
        # get cropped image
        img = frame[config.cropHeightStart:config.cropHeightEnd, 0:config.camWidth]

        # keep un-edited copy of the image
        img2 = img

        # run canny edge detector on image
        img = cv2.Canny(img, config.cannyLeft, config.cannyRight)

        # run opencv find contours, only external boxes
        (contours, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # run contour sort method
        contours = sort_contours.main(contours)

        # return un-edited image and contours
        return img2, contours
