version = "1.0"

# AutomationHat
automation = 1

# Camera Settings
camWidth = 800
camHeight = 480
camFrameRate = 90

# Crop Settings
cropWidth = 800
cropHeight = 150
cropHeightStart = 145
cropHeightEnd = cropHeightStart + cropHeight
cropArea = cropHeight * camWidth

# Image Manipulation Settings
edgesGap = 20
cannyMin = 100
cannyMax = 900
threshLimit = 128

# Alarm Settings
whiteThresh = 70
alarmTime = 4
minBlobCount = 6
