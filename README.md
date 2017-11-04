# OCR-Project
OpenCV OCR Project

## Install process:
**1. Clone and update the repository**

Open terminal in Pi. And copy/paste the following:

``git clone https://github.com/philLITERALLY/OCR-Project.git``

Then navigate to this new folder:

``cd OCR-Project``

Update this folder:

``git remote update``

Checkout this branch (Final Version Non-OCR):

``git checkout nonOCR``

You will now have the final version of the app.

**2. Install CV2:**

``sudo apt-get install python-opencv``

**3. Install ImageTk:**

``sudo apt-get install python-imaging-tk``

**4. Install RPi Camera:**

``sudo apt-get update``

``sudo apt-get upgrade``

``sudo rpi-update``

``reboot``

**5. Install AutomationHat (not required but used for alarm):**

``curl https://get.pimoroni.com/automationhat | bash``

**6. Make application boot on start-up:**

``nano /home/pi/.config/lxsession/LXDE-pi/autostart``

Add the following to the bottom of the file:

``@/usr/bin/python /home/pi/OCR-Project/main.py``

**7. Remove screensaver:**

Install the X Windows screensaver application:

``sudo apt-get install xscreensaver``

Once this has been installed, you can find the screensaver application under the Preferences option on the main desktop menu. This provides options for disabling the screensaver and power saving mode.
