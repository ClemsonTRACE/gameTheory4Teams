# from django.test import TestCase
from selenium import webdriver
import requests
import json
import time

# Create your tests here.

def frontend_test():
	browser = webdriver.Chrome()
	# browser.get("https://lbarberiscanoni.github.io/gt4teams_frontend/#/bos/human/ppo")
	browser.get("localhost:3000/#/bos/human/ppo")
	forwardBtn = browser.find_element_by_class_name("btn")
	forwardBtn.click()
	time.sleep(2)
	confirmBtn = browser.find_element_by_class_name("btn")
	confirmBtn.click()
	time.sleep(2)
	moveBtn = browser.find_element_by_class_name("btn")
	for i in range(30):
		moveBtn.click()
		browser.switch_to.alert.accept()
		time.sleep(4)
		try:
			browser.switch_to.alert.accept()
		except:
			time.sleep(2)
			browser.switch_to.alert.accept()

	browser.close()

def backend_test():
	test_state = {
			"game": "3pd",
			"opponent": "ai",
			"model": "ppo",
			"status": False, 
			"numEpochs": 2,
			"numTurns": 9,
			"gameState": {},
			"payoffs": {},
			"epoch": 0,
			"turn": 0,
			"surveyID": "don't matter",
			"move": 0
		}

	for x in range(test_state["numEpochs"] + 1):
		test_state["gameState"][x] = {}
		test_state["payoffs"][x] = {}

		for y in range(test_state["numTurns"] + 1):
			test_state["gameState"][x][y] = {}
			test_state["payoffs"][x][y] = {}

			test_state["gameState"][x][y] = [0, 0, 0]
			test_state["payoffs"][x][y] = [0, 0, 0]


	r = requests.post('http://localhost:8000/games/3pd/ppo', data = json.dumps(test_state))

backend_test()