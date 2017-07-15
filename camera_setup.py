# import packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# import my modules
import config

def main():
    # init camera
    camera = PiCamera()
    camera.resolution = (config.camWidth, config.camHeight)
    camera.framerate = config.camFrameRate
    camera.color_effects = (128, 128)
    camera.shutter_speed = 1800

    # init cap
    rawCap = PiRGBArray(camera, size = (config.camWidth, config.camHeight))

    stream = camera.capture_continuous(rawCap, format="bgr",
	use_video_port=True)

    # return camera and init cap
    return stream, rawCap
