import sys
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

parent_dir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )

sys.path.append(parent_dir)

import AutoSufer

class YoutubeAS(AutoSufer):
    def open(self):
        self.driver.get("https://www.youtube.com")
    
    def focus_search(self, xpath):
        search_bar = self.focus('//*[@id="search"]')
        
        print(search_bar.text)

yt = YoutubeAS()