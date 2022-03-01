from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from threading import Thread

class DebtCollector(Thread):
    def __init__(self, username="", password="", secret=""):
        Thread.__init__(self)
        self.URL = "https://www.manage-student-loan-balance.service.gov.uk/ors/account-overview/secured/summary?_locale=en"
        self.LOGIN_URL = "https://logon.slc.co.uk/welcome/secured/login?svc=ors&_locale=en_GB_GOVUK"
        self.LOGIN_SECRET_URL = "https://logon.slc.co.uk/welcome/secured/login-secret-answer?cookieConsent=accept"
        self.username = username
        self.password = password
        self.secret = secret
        self.debt = ""
    
    def wait_till_id(self, driver, id, timeout=2):
        try:
            element_present = EC.presence_of_element_located((By.ID, id))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            raise TimeoutException
        finally:
            pass
    
    def run(self):
        driver: Firefox = webdriver.Firefox()
        driver.get(self.URL)
        
        while True:
            try:
                self.wait_till_id(driver, "balanceId_1", timeout=3)
                
                amount = driver.find_element(By.ID, "balanceId_1").text
                
                assert amount != ""
                
                if self.debt != amount:
                    self.debt = amount
                print(f"Your debt is: {self.debt}")
            except (NoSuchElementException, TimeoutException, AssertionError) as e:
                if driver.current_url == self.LOGIN_URL:
                    driver.find_element(By.ID, "userId").send_keys(self.username)
                    driver.find_element(By.ID, "password").send_keys(self.password)
                    driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

                    self.wait_till_id(driver, "title-secret-answer")

                    driver.find_element(By.ID, "secretAnswer").send_keys(self.secret)
                    driver.find_element(By.ID, "secretAnswer").send_keys(Keys.ENTER)

                    continue
                else:
                    print(f"Program has experienced a fatal error. Here is the message:\n{e.msg}")
                    break
            sleep(60)
        
th = DebtCollector("", "", "")
th.start()

