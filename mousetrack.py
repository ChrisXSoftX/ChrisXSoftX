#!python3
'''I wonder why it is working'''
import pyautogui
import time

print('Press Ctrl-C to quit')

try:  
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'

        print('\r' + positionStr, end='', flush=True)  # refresh line
        time.sleep(0.1)  # reduce CPU usage
except KeyboardInterrupt:
    print('\nDone.')
