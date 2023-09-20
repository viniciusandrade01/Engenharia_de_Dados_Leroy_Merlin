from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GeneralSelenium:
    def __init__(self):
        pass

    def startSelenium(self):
        return webdriver.Chrome()

    def navegateUrl(self, driver, url):
        return driver.get(url)

    def getTitle(self, driver):
        return driver.title

    def waiting(self, driver, time: int):
        driver.implicitly_wait(time)

    def ClosingSelenium(self):
        return webdriver.Chrome()