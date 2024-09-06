# ----------------------------------------------------------------------
#								Imports
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
#   							Globals
# ----------------------------------------------------------------------

pyautogui.FAILSAFE = True
TOKEN = 'your_clash_api_key'

# ----------------------------------------------------------------------
#   							 Main
# ----------------------------------------------------------------------
class Members():
	def __init__(self):
		self.token = TOKEN
		self.header = {
			'Accept' : 'application/json',
			'authorization' : 'Bearer ' + self.token 
		}
		
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

		self.player_positions = {
			'1' : (252, 525),
			'2' : (251, 637),
			'3' : (253, 768),
			'4' : (249, 897),
			'5' : (250, 1002),
		}

		self.keyboard = Controller()
		self.added = 0
		self.count = 0
		self.invited = []
		self.scroller = 0
		self.start()	

	def start(self):
		self.count = input('Number of players to invite: ')
		time.sleep(5)
		for _ in range(100):
			for i in range(3):
				if i == 0:
					self.begin('war')
				if i == 1:
					self.begin('league')
				if i == 2:
					self.begin('trophy')

	def begin(self, search):
		# Navigate to member area
		time.sleep(1)
		pyautogui.click(self.positions['game_area'])
		time.sleep(1)

		self.keyboard.press('g')
		self.keyboard.release('g')
		time.sleep(1)

		pyautogui.click(self.positions['my_clan'])
		time.sleep(1)

		pyautogui.click(self.positions['find_new_members'])
		time.sleep(1)		

		# Select filter
		if search == "war":
			time.sleep(1)
			pyautogui.click(self.positions['filter_wars'])
			time.sleep(1)

		if search == "league":
			time.sleep(1)
			pyautogui.click(self.positions['filter_league'])
			time.sleep(1)

		if search == "trophy":
			time.sleep(1)
			pyautogui.click(self.positions['filter_trophy'])
			time.sleep(1)		

		# Search
		pyautogui.click(self.positions['search_suggested'])
		time.sleep(1)

		# Invite players
		self.invitations()
		
	def invite(self):
		try:
			x, y = pyautogui.locateCenterOnScreen('invite.png', confidence=.8)
			pyautogui.click(x, y)
		except Exception as e:
			return

		self.added += 1
		print("[invited] " + str(self.added))
		if (int(self.added) >= int(self.count)):
			print("[FINISHED]")
			self.leave()
			sys.exit() # finished adding all players	

	def invitations(self):
		# send invite to player_positions
		amount = len(self.player_positions) + 1
		
		for _ in range(12): # page drag down amount
			for i in range(1, amount):
				time.sleep(1.5)
				
				# click profile
				pyautogui.click(self.player_positions[str(i)]) 
				time.sleep(2)

				# send player invite
				if self.filter() == True:
					self.invite()
					time.sleep(1.5)

				try:
					x, y = pyautogui.locateCenterOnScreen('back.png', confidence=.8)
					pyautogui.click(x, y)
				except Exception as e:
					return

			# drag to next section, restart function: run in loop 10 times
			pyautogui.moveTo(self.player_positions['5'])
			time.sleep(1.5)
			pyautogui.dragTo(247, 480, 2, button='left')
			time.sleep(1.5)

	def finished(self):
		# Added all players from selected filter
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)
		
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)	

	def leave(self):
		# finished inviting all players
		try:
			x, y = pyautogui.locateCenterOnScreen('exit.png', confidence=.8)
			pyautogui.click(x, y)
		except Exception as e:
			print('failed to exit')		

	# ------------------------------------------------------------------
	#						Player Filtering
	# ------------------------------------------------------------------

	def filter(self):
		# filter driver function
		self.get_info()
		
		# passes all filters
		try:
			f_clan = self.clan()
			f_level = self.level()

			if f_clan == False or f_level == False:
				return False

		except Exception as e:
			return False

		self.invited.append(str(self.player.get('name')))
		return True

	def get_info(self):
		# copy player id
		time.sleep(1)
		pyautogui.click(self.positions['player_code'])
		time.sleep(0.7)
		pyautogui.click(self.positions['copy'])

		# get player information
		player_id = str(pc.paste())
		search = f'https://api.clashofclans.com/v1/players/%23{player_id[1:]}'.format()
		self.player = requests.get(search, headers = self.header).json()

	def clan(self):
		# Do they pass clan filtering
		try:
			c = self.player.get('clan')
			name = c['name']
			if len(name) > 1:
				return False
		except Exception as e:
			return True
		return True

	def level(self):
		# Check their level & townhall
		th = self.player.get('townHallLevel')
		lvl = self.player.get('expLevel')

		if th == 8 and lvl >= 65:
			return True
		elif th == 9 and lvl >= 75:
			return True
		elif th == 10 and lvl >= 85:
			return True
		elif th == 11 and lvl >= 100:
			return True
		elif th > 11 and lvl >= 120:
			return True
				
		return False


clash = Members()
