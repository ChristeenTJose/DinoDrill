from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import cv2
import numpy as np
		
def Empty(x):
	pass
	
def play():
	url = 'chrome://dino/'
	driver = webdriver.Chrome()
	try:
		driver.get(url) #selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_INTERNET_DISCONNECTED
	except:	
		body = driver.find_element_by_tag_name('body')
		
		FRAME_DELAY = 1 #in ms
		
		cv2.namedWindow('Caliberate')
		cv2.createTrackbar('L_HUE', 'Caliberate', 0, 179, Empty)
		cv2.createTrackbar('L_SAT', 'Caliberate', 0, 255, Empty)
		cv2.createTrackbar('L_VAL', 'Caliberate', 0, 255, Empty)
		cv2.createTrackbar('U_HUE', 'Caliberate', 0, 179, Empty)
		cv2.createTrackbar('U_SAT', 'Caliberate', 0, 255, Empty)
		cv2.createTrackbar('U_VAL', 'Caliberate', 0, 255, Empty)
	
		cv2.createTrackbar('L_REG', 'Caliberate', 0, 279, Empty)
		#the minimum limit is always zero (https://docs.opencv.org/3.4/da/d6a/tutorial_trackbar.html)
		cv2.createTrackbar('W_REG', 'Caliberate', 0, 200, Empty)
	
		cv2.setTrackbarPos('U_HUE', 'Caliberate', 179)
		cv2.setTrackbarPos('U_SAT', 'Caliberate', 255)
		cv2.setTrackbarPos('U_VAL', 'Caliberate', 255)
	
		cv2.setTrackbarPos('L_REG', 'Caliberate', 130)
		cv2.setTrackbarPos('W_REG', 'Caliberate', 125)
	
		vc = cv2.VideoCapture(0)
		key_pressed = cv2.waitKey(FRAME_DELAY)
		Went_Down = 0
		Duck = 0
		STARTED = 0
		while key_pressed & 0xFF != ord('q'):
			return_value, frame=vc.read()
			frame = np.flip(frame, 1)
			
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			
			L_HUE = cv2.getTrackbarPos('L_HUE', 'Caliberate')
			L_SAT = cv2.getTrackbarPos('L_SAT', 'Caliberate')
			L_VAL = cv2.getTrackbarPos('L_VAL', 'Caliberate')
			U_HUE = cv2.getTrackbarPos('U_HUE', 'Caliberate')
			U_SAT = cv2.getTrackbarPos('U_SAT', 'Caliberate')
			U_VAL = cv2.getTrackbarPos('U_VAL', 'Caliberate')
		
			Lower = [L_HUE, L_SAT, L_VAL]
			Upper = [U_HUE, U_SAT, U_VAL]
			
			L_REG = 479 - cv2.getTrackbarPos('L_REG', 'Caliberate')
			W_REG = cv2.getTrackbarPos('W_REG', 'Caliberate')
			LIMIT = L_REG - W_REG
		
			mask = cv2.inRange(hsv, np.array(Lower), np.array(Upper))
			mask_BGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
		
			contours,hierarchy=cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
			if contours:	
				c = max(contours, key = cv2.contourArea)
				cv2.drawContours(mask_BGR, c, -1, (0, 102, 255), 3)
				area = cv2.contourArea(c)
				#print(area)
				if area > 1000:
					x,y,W,H = cv2.boundingRect(c)
					#cv2.rectangle(mask_BGR, (x, y), (x + W, y + H), (0, 102, 255), 1)
					center_x = x + W//2
					center_y = y + H//2
					cv2.circle(mask_BGR, (center_x, center_y), 4, (0, 0, 255), -1)
					
					if STARTED:
						if center_y < LIMIT:
							if Went_Down == 1:
								body.send_keys(Keys.SPACE) #MOST IMPORTANT LINE
								Went_Down = 0
						elif center_y < L_REG:
							Went_Down = 1
							Duck = 0
						else:
							if Duck == 0:
								body.send_keys(Keys.ARROW_DOWN) #Code is correct, Keys.SPACE works 
								#print('Down button pressed')
								Duck = 1
			
			cv2.putText(mask_BGR, 'Ground', (10, LIMIT + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
			cv2.putText(mask_BGR, 'Air', (10, LIMIT - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
			#cv2.putText(mask_BGR, 'Duck', (10, L_REG + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
			
			display = np.hstack((frame, mask_BGR))
			cv2.rectangle(display, (0, LIMIT), (1279, L_REG), (0, 255, 0), 4)
			cv2.imshow('Display', display)
		
			if key_pressed & 0xFF == ord('s'): 
				if STARTED == 0:
					STARTED = 1
					element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'runner-canvas')))
				body.send_keys(Keys.SPACE)
			
			elif key_pressed & 0xFF == ord('d'): 
				if STARTED:
					body.send_keys(Keys.ARROW_DOWN)
			
			key_pressed = cv2.waitKey(FRAME_DELAY)	
		vc.release()
		cv2.destroyAllWindows()
	finally:
		driver.quit()
				

if __name__ == '__main__':
	play()
