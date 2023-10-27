import time
import random
import pathlib
from os import listdir
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

MAX_TIME_WAIT = 4

class FileSufer:
    def __init__(self, browser_driver):
        self.driver = browser_driver
        self.driver.implicitly_wait(MAX_TIME_WAIT)
        self.driver.execute_script("window.scrollTo(0, 300)")

    def open_file(self, file_url):
        self.driver.get(file_url)

class PersonalWebTest(FileSufer):
    def get_form_element(self):
        return self.driver.find_element(By.ID, "thought")
    
    def get_submit_button_element(self):
        return self.driver.find_element(By.ID, "sbtn")
    
    def populate_form(self,text):
        self.get_form_element().send_keys(text)

    def submit_form(self):
        self.get_submit_button_element().click()

    def test_send_message(self):
        self.get_form_element()
        self.populate_form("Some Text Here")
        self.submit_form()
        self.driver.implicitly_wait(MAX_TIME_WAIT)

        if len( str(self.get_form_element().get_attribute("value")) ) > 0:
            print("input has not been cleared")


def main():
    filename_to_test = 'index.html'
    directory_to_test = pathlib.Path(__file__).parent.parent.parent.resolve()

    print("file://" + str(directory_to_test).replace('\\', '/') + "/" + filename_to_test)

    test = PersonalWebTest(webdriver.Chrome())
    test.open_file("file://" + str(directory_to_test).replace('\\', '/') + "/" + filename_to_test)

    test.test_send_message()
    
    while True:
        pass

if __name__ == "__main__":
    main()