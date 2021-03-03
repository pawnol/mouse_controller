import mouse
import pyautogui
import serial

X_CENTER = Y_CENTER = 512
CURRENT_POSITION = pyautogui.position()
SENSITIVITY = 40
ARDUINO_PORT = 'COM4'
BAUD_RATE = 9600
TIME_OUT = 5
SWITCH_BUFFER = 7

# FUNCTIONS

def checkTolerance(position, tolerance = 1):
    if abs(position) <= tolerance:
        return 0
    else:
        return position


#MAIN

mouseX = CURRENT_POSITION[0]
mouseY = CURRENT_POSITION[1]
port = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout = TIME_OUT)

startRead = False
while not startRead:
    port.write(b'S')
    startUpByte = port.readline(1).decode()
    if startUpByte == "S":
        startRead = True

mouseTimeOut = False
currentMouseClick = 0
while True:
    serialData = port.readline().decode().strip().split(',')
    print(serialData)
    if (serialData[0].isnumeric() and serialData[1].isnumeric()
            and serialData[2].isnumeric()):
        joystickX = int(serialData[0])
        joystickY = int(serialData[1])
        button = int(serialData[2])
        dx = checkTolerance((int(joystickX) - X_CENTER) / SENSITIVITY, 0.5)
        dy = checkTolerance((Y_CENTER - int(joystickY)) / SENSITIVITY, 0.5)
        mouseX += dx
        mouseY += dy
        mouse.move(mouseX, mouseY)
        if (button == 1 and not mouseTimeOut):
            mouse.click()
            mouseTimeOut = True
        elif (mouseTimeOut and currentMouseClick < SWITCH_BUFFER):
            currentMouseClick += 1
        else:
            mouseTimeOut = False
            currentMouseClick = 0