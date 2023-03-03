from ppadb.client import Client
import pytesseract
import cv2

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


custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(screen, config=custom_config)
print(text)

# co ten program musi wypluć:
# - Wartość początkowa
# - Wartość końcowa
# - Liczba przycisków
# - Poszczególne przyciski