import os
from selenium import webdriver
from urllib.request import urlretrieve

# chrome_driver_filename = "chromedriver_win32.zip"
# if os.name == 'posix':
#     chrome_driver_filename = "chromedriver_linux64.zip"

# chrome_version = "117.0.5938.132"

# chrome_driver_download_uri = "https://chromedriver.storage.googleapis.com/index.html?path="

# chrome_driver_download_uri += chrome_version + "/" + chrome_driver_filename

# urlretrieve(chrome_driver_download_uri, chrome_driver_filename)

driver = webdriver.Chrome()

url = "https://mybk.hcmut.edu.vn/my/homeSSO.action"

driver.get(url)

print(driver.title)
