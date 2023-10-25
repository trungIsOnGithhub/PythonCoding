import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# parent_dir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )

# sys.path.append(parent_dir)

# import AutoSufer

MAX_TIME_WAIT = 300

class AutoSufer:
	def __init__(self, browser_driver   ):
		self.driver = browser_driver
	
	def click_button(xpath):
		button = self.driver.find_element(By.XPATH, xpath)

		button.click()

	def open_url(self, url):
		self.driver.get(url)

	def open_google(self):
		self.driver.get('https://google.com')
  
	def focus(self, xpath):
		return self.driver.find_element(By.XPATH, xpath)

class YoutubeAS(AutoSufer):
    def open(self):
        self.open_url("https://www.youtube.com")
    
    def focus_search(self):
        search_bar = self.focus('//*[@id="search"]')
        print(search_bar.text)
		
    def open_specific_video_at_specific_time(self, url, start_minute, start_second):
        start_time_in_second = start_minute * 60 + start_second
        start_time_query_string = str(start_time_in_second) + "s" # in second

        if not isinstance(url, str):
            print("Invalid URL!")
            exit()
        
        try:
            url.index("?")
        except ValueError as VExp:
            print("Invalid URL!")
            exit()

        url += "&t=" + start_time_query_string
        self.driver.get(url)

        play_btn = WebDriverWait(self.driver, MAX_TIME_WAIT).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Play (k)']")))
        play_btn.click()
        print('-----')
        video_duration_holder = self.driver.find_element(By.CLASS_NAME, 'ytp-time-duration')
        video_duration_text = video_duration_holder.text

        print(video_duration_text)

        text_splited_arr = video_duration_text.split(':')

        if len(text_splited_arr) > 2:
            print("Too long video!")
            exit()

        video_duration = int(text_splited_arr[0]) * 60 + int(text_splited_arr[1])

        time.sleep(video_duration + 5 - start_time_in_second)

        # try:
        #     ended_video_element = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.CLASS, "ended-mode")))
        # except Exception as err:
        #     self.open_specific_video_at_specific_time(url, start_minute, start_second)         

        # if ended_video_element is not None:
        #     self.open_specific_video_at_specific_time(url, start_minute, start_second)
 
    def skip_to(self):
        # pause_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Pause (k)']")))
        # pause_btn.click()

        # comment out to test pause btn, otherwise it happens so fast you don't notice
        play_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Play (k)']")))
        # play_btn.click()
        # mute_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Mute (m)']")))
        # mute_btn.click()

        # # comment out to test mute_btn, otherwise it happens so fast you don't notice it
        # unmute_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Unmute (m)']")))
        # unmute_btn.click()
        
        # driver.find_element_by_css_selector('body').send_keys(Keys.SPACE)
        # time.sleep(5)
        num_of_skip = int(duration_of_skip / 5)

        for i in range(0,num_of_skip):
            self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.RIGHT)

        play_btn.click()
        
        time.sleep(69)

playlist = [
      ['https://www.youtube.com/watch?v=8M6hwcCr4_E', 2, 3],
      ['https://www.youtube.com/watch?v=nPUQCBugSaw', 0, 3]
]

yt = YoutubeAS(webdriver.Chrome())

for video in playlist:
    yt.open_specific_video_at_specific_time(video[0], video[1], video[2])