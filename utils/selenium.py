from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GeneralSelenium:
    def __init__(self, driver_path, base_url=''):
        self.driver_path = driver_path
        self.base_url = base_url
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def close(self):
        if self.driver:
            self.driver.quit()

    def navigate_to_url(self, url):
        if not self.driver:
            self.start()
        self.driver.get(url)

    def click_button(self, selector):
        wait = WebDriverWait(self.driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()

    def find_element_by_css_selector(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def find_elements_by_css_selector(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)
    
#if __name__ == "__main__":
#    # Exemplo de uso
#    driver_path = '/caminho/para/o/driver/chromedriver.exe'
#    base_url = 'https://exemplo.com'
#    
#    selenium = GeneralSelenium(driver_path, base_url)
#    
#    try:
#        selenium.navigate_to_url(base_url)
#        selenium.click_button('seletor-do-botao')
#        
#        # Realize outras operações com o Selenium conforme necessário
#        element = selenium.find_element_by_css_selector('seletor-do-elemento')
#        element.click()
#    
#    finally:
#        selenium.close()
