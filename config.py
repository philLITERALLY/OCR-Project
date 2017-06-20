version = "0.1"

helpText = ["--help", "--h", "-h"]

responsesFile = "/home/pi/OCR-Project/training/responses.dat"
samplesFile = "/home/pi/OCR-Project/training/samples.dat"

camWidth = 640
camHeight = 480
camFrameRate = 32
cropHeightStart = 100
cropHeightEnd = 200
cannyLeft = 300
cannyRight = 700
edgesGap = 20

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
