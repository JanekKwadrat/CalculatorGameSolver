from ppadb.client import Client
import pytesseract
import cv2
import numpy as np

def connect_device():
	adb = Client(host='127.0.0.1',port=5037)
	devices = adb.devices()
	if len(devices) == 0:
		print("No Devices Attached")
		quit()
	return devices[0]

def take_screenshot(device):
	image = device.screencap()
	with open('screen.png', 'wb') as f:
		f.write(image)

device = connect_device()
take_screenshot(device)
screen = cv2.imread('screen.png')


# 264,198 - 416, 242
moves = screen[198:242, 264:416]
goal  = screen[198:242, 483:608]
init  = screen[323:485, 87:633]
dsize = (136, 40)
init = cv2.resize(init, dsize)

butt1 = screen[709:848, 270:447]
butt2 = screen[934:1057, 270:447]
butt3 = screen[934:1057, 491:668]
butt4 = screen[1137:1272, 270:447]
butt5 = screen[1137:1272, 491:668]


custom_config = r'--oem 1 --psm 7 -l eng+equ --tessdata-dir . outputbase digits'
dumber_config = r'--oem 1 --psm 7 -l letsgodigital --tessdata-dir . tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(moves, config=custom_config)
print(text)
text = pytesseract.image_to_string(goal, config=custom_config)
print(text)
text = pytesseract.image_to_string(init, config=dumber_config)
print(text)
text = pytesseract.image_to_string(butt1, config=custom_config)
print(text)
text = pytesseract.image_to_string(butt2, config=custom_config)
print(text)
text = pytesseract.image_to_string(butt3, config=custom_config)
print(text)
text = pytesseract.image_to_string(butt4, config=custom_config)
print(text)
text = pytesseract.image_to_string(butt5, config=custom_config)
print(text)



# co ten program musi wypluć:
# - Wartość początkowa
# - Wartość końcowa
# - Liczba przycisków
# - Poszczególne przyciski