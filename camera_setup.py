# import packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# import my modules
import config

def main():
    # init camera
    camera = PiCamera()
    # set camera resolution to config value
    camera.resolution = (config.camWidth, config.camHeight)
    # set camera framerate to config value
    camera.framerate = config.camFrameRate
    # set camera to black and white
    camera.color_effects = (128, 128)
    # set shutter_speed to config value
    camera.shutter_speed = config.shutterSpeed
    # camera.brightness = 90

    # init capture
    rawCap = PiRGBArray(camera, size = (config.camWidth, config.camHeight))

    # initiate camera stream
    stream = camera.capture_continuous(rawCap, format="bgr",
	   use_video_port=True)

    # return camera stream and init cap
    return stream, rawCap, camera
