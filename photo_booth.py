# import the necessary packages
from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import time
import config

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=True, resolution=(config.camWidth, config.camHeight), framerate=90).start()
time.sleep(2.0)

# start the app
pba = PhotoBoothApp(vs)
pba.root.mainloop()
