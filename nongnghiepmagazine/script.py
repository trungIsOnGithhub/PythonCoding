import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

MAX_TIME_WAIT = 300
TIME_TO_FULL_LOAD = 10
READING_TIME = 3000

class AutoSufer:
    def __init__(self, browser_driver):
        self.driver = browser_driver
	
    def click_button(self, xpath):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()

    def open_url(self, url):
        self.driver.get(url)

    def open_google(self):
        self.driver.get('https://google.com')

class NongNghiepMagazineAS(AutoSufer):
    def open(self):
        self.open_url("https://nongnghiep.vn/emagazine-multimedia/")
        self.driver.implicitly_wait(TIME_TO_FULL_LOAD)
		
    def get_landing_page_titles(self):
        title_element_list = self.driver.find_elements(By.CSS_SELECTOR, ".main-title > a")
        num_element = len(title_element_list)
        element_random_pick = random.randint(0, num_element-1)
        title_element_list[element_random_pick].click()
        self.driver.implicitly_wait(10)

    def wait_reading_article(self):
        self.driver.implicitly_wait(READING_TIME)

    def hide_article_text(self):
        self.driver.execute_script('document.querySelectorAll("p").forEach(function(element){ element.style.visibility = "hidden" });')
	
magazine = NongNghiepMagazineAS(webdriver.Chrome())

magazine.open()
magazine.get_landing_page_titles()
magazine.hide_article_text()
# magazine.wait_reading_article()
while True:
    pass