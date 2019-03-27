from django.test import TestCase
from selenium import webdriver
import time

# Create your tests here.
browser = webdriver.Chrome()
browser.get("http://localhost:3000/#/bos/human/ppo")
forwardBtn = browser.find_element_by_class_name("btn")
forwardBtn.click()
time.sleep(2)
moveBtn = browser.find_element_by_class_name("btn")
for i in range(5):
	moveBtn.click()
	browser.switch_to.alert.accept()
	time.sleep(4)
	try:
		browser.switch_to.alert.accept()
	except:
		time.sleep(2)
		browser.switch_to.alert.accept()

browser.close()
