# import packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def main(config):
    # init camera
    camera = PiCamera()
    camera.resolution = (config.camWidth, config.camHeight)
    camera.framerate = config.camFrameRate
    camera.color_effects = (128, 128)

    # init cap
    rawCap = PiRGBArray(camera, size = (config.camWidth, config.camHeight))

    # camera warmup
    time.sleep(0.1)

    # return camera and init cap
    return camera, rawCap
