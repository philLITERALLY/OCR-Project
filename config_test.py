version = "0.1"

helpText = ["--help", "--h", "-h"]

responsesFile = "/home/pi/OCR-Project/training/responses.dat"
samplesFile = "/home/pi/OCR-Project/training/samples.dat"

automation = False

camWidth = 800
camHeight = 480
camFrameRate = 90
cropWidth = 800
cropHeight = 150
cropHeightStart = 145
cropHeightEnd = cropHeightStart + cropHeight
cannyLeft = 100
cannyRight = 900
edgesGap = 20
cropArea = cropHeight * camWidth

threshLimit = 128
whiteThresh = 70
alarmTime = 20
minBlobCount = 2

# print help options
def printHelp():
    print("------------------------------------------------------")
    print("Program to read and recognize printed text with OpenCV")
    print("------------------------------------------------------\n")
    
    print("Version: " + version)
    print("Usage:\n")
    
    print("  -r            - Run OCR")
    print("  While running :")
    print("    `           - Stop program\n")
    
    print("  -h/--h/--help - This help guide")
    
    print("  --clear_learn - Clear previously learned OCR\n")
    
    print("  --learn       - Start learning mode")
    print("  While running :")
    print("    TAB         - Learn current screen")
    print("    SPACE       - Skip displayed letter")
    print("    `           - Stop program")
