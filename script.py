import os
from selenium import webdriver

chrome_driver_file_linux = "chromedriver_linux64.zip"

chrome_driver_file_windows = "chromedriver_win32.zip"

chrome_driver_base_uri = "https://chromedriver.storage.googleapis.com/index.html?path=108.0.5359.22/"

chrome_driver_base_download_uri = chrome_driver_base_uri

if os.name == 'nt':
    chrome_driver_base_download_uri += chrome_driver_file_windows
elif os.name == 'posix':
    chrome_driver_base_download_uri += chrome_driver_file_linux

#driver = webdriver.Chrome()

#driver.get("https://mybk.hcmut.edu.vn/my/homeSSO.action")

print(chrome_driver_base_download_uri)
