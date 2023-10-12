from selenium import webdriver
from selenium.webdriver.common.by import By

class AutoSufer:
	def __init__(self, browser_driver):
		self.driver = browser_driver
	
	def click_button(xpath):
		button = self.driver.find_element(By.XPATH, xpath)

		button.click()

	def open_url(url):
		self.driver.get(url)

	def open_google(url):
		self.driver.get('https://google.com')