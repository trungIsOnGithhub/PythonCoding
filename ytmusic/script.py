import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# parent_dir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )

# sys.path.append(parent_dir)

# import AutoSufer

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
  
	def focus(self, xpath):
		return self.driver.find_element(By.XPATH, xpath)

class YoutubeAS(AutoSufer):
    def open(self):
        self.driver.get("https://www.youtube.com")
    
    def focus_search(self, xpath):
        search_bar = self.focus('//*[@id="search"]')
        
        print(search_bar.text)
        
    def other(self):
        # pause_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Pause (k)']")))
        # pause_btn.click()
        self.driver.get('https://www.youtube.com/watch?v=IeR2g9692sM')

        # comment out to test pause btn, otherwise it happens so fast you don't notice
        play_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Play (k)']")))
        play_btn.click()

        # mute_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Mute (m)']")))
        # mute_btn.click()

        # # comment out to test mute_btn, otherwise it happens so fast you don't notice it
        # unmute_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Unmute (m)']")))
        # unmute_btn.click()
        
        # driver.find_element_by_css_selector('body').send_keys(Keys.SPACE)
        # time.sleep(5)
        for i in range(0,10):
            self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.RIGHT)
        
        time.sleep(69)

yt = YoutubeAS(webdriver.Chrome())
yt.other()