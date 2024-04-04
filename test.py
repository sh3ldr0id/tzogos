from pyautogui import position, leftClick, screenshot, locateCenterOnScreen
from PIL.ImageShow import show
from matplotlib.pyplot import imshow, show
from time import sleep

sleep(5)

print(position())

img = screenshot(region=(712, 330, 1213-712, 508-330))

imshow(img)
show()