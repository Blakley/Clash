# ==================== imports =======================
import os
import re
import sys
import cv2
import json
import time
import requests
import pyautogui
import pytesseract 
import numpy as np
import pyperclip as pc
from PIL import Image 
from pynput.keyboard import Key, Controller


pyautogui.FAILSAFE = True

# ==================== Main Class ====================
class Clash():
	def __init__(self):
		self.positions = {
			'game_area' : 			(1373, 35),
			'my_clan' : 			(809, 66),
			'find_new_members': 	(516, 733),
			'filter_wars': 			(396, 298),
			'filter_league': 		(802, 296),
			'filter_trophy': 		(1249,301),
			'search_suggested': 	(1548,426),
			'player_area': 			(253, 501),	
			'player_code': 			(757, 286),
			'copy': 				(946, 300),
		}
		# api token
		self.token = 'your_clash_api_token'
		self.header = {
			'Accept' : 'application/json',
			'authorization' : 'Bearer ' + self.token 
		}
		self.keyboard = Controller()
		self.added = 0
		self.count = 0
		self.init()
	
	# starter function
	def init(self):
		self.count = input('How many players to invite: ')
		time.sleep(5)
		for _ in range(20):
			for i in range(3):
				if i == 0:
					if self.start('war') == 1:
					 	return
				if i == 1:
					if self.start('league') == 1:
						return
				if i == 2:
					if self.start('trophy') == 1:
						return	

	# Filter players by various criteria
	def filter(self):
		# copy player_id code
		time.sleep(1)
		pyautogui.click(self.positions['player_code'])
		time.sleep(0.7)
		pyautogui.click(self.positions['copy'])

		# lookup player info
		player_id = str(pc.paste())
		search = f'https://api.clashofclans.com/v1/players/%23{player_id[1:]}'.format()
		response = requests.get(search, headers = self.header).json()

		# name filter
		player_name = response.get('name')
		RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
		nochinese = RE.sub('', player_name)
		if nochinese != player_name:
			return False

		# townhall filter
		town_hall = response.get('townHallLevel')
		if int(town_hall) < 9:
			return False

		# trophy filter
		trophies = response.get('trophies')
		if int(trophies) < 1200:
			return False

		# troops filter
		'''
		troops = response.get('troops')
		barb = troops[0]
		archer = troops[1]
		if int(archer['level']) < 4 and int(barb['level']) < 4:
			return False 

		balloon = troops[5]	
		if int(balloon['level']) < 4:
			return False 
		
		dragon = troops[8]
		if int(dragon['level']) < 3:
			return False 
		'''

		return True

	# invites a player
	def invite(self):
		try:
			x, y = pyautogui.locateCenterOnScreen('images/invite.png')
			pyautogui.click(x, y)
		except Exception as e:
			return

		self.added += 1
		print("added: " + str(self.added))
		if (self.added == self.count):
			print("finished")
			return 1

	# stars the program
	def start(self, search_filter):
		# navigate to game window
		time.sleep(1)
		pyautogui.click(self.positions['game_area'])
		time.sleep(1)

		# press G to open profile
		self.keyboard.press('g')
		self.keyboard.release('g')
		time.sleep(1)

		# click my clan button
		pyautogui.click(self.positions['my_clan'])
		time.sleep(1)

		# click find new members button
		pyautogui.click(self.positions['find_new_members'])
		time.sleep(1)
		
		# select filter
		if search_filter == "war":
			time.sleep(1)
			pyautogui.click(self.positions['filter_wars'])
			time.sleep(1)

		if search_filter == "league":
			time.sleep(1)
			pyautogui.click(self.positions['filter_league'])
			time.sleep(1)

		if search_filter == "trophy":
			time.sleep(1)
			pyautogui.click(self.positions['filter_trophy'])
			time.sleep(1)


		# click search button
		pyautogui.click(self.positions['search_suggested'])
		time.sleep(1)

		# move mouse to player area:
		pyautogui.moveTo(self.positions['player_area'])
		time.sleep(1)

		# add the players
		last_pos = self.positions['player_area']
		for x in range(40):				
			# 1. click user profile & try to click again 
			pyautogui.click()
			time.sleep(0.5)
			
			try:
				pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 10)
			except Exception as e:
				continue

			pyautogui.click()
			time.sleep(1.5)

			# 2. invite player if they meet all qualifications
			if self.filter() == True:
				status = self.invite()
				if status == 1:
					return 1 # finished adding players

			time.sleep(1)

			# 3. go back to menu
			self.keyboard.press(Key.esc)
			self.keyboard.release(Key.esc)
			time.sleep(1)

			# 4. reposition mouse to last position
			pyautogui.moveTo(last_pos)
			time.sleep(1)

			# 5. scroll to next profile
			pyautogui.scroll(-20)
			time.sleep(1)

			# 6. update last position
			last_pos = pyautogui.position()
			time.sleep(1)

		# --------- Finished ---------
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)	
		return 0


# starter code
clash = Clash()