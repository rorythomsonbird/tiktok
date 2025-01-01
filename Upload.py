from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time

class Upload:
    def send_message():
        
        url = f"https://www.tiktok.com/" #URL
        options = webdriver.ChromeOptions()
        options = ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.204 Safari/537.3')
        options.add_argument('--window-size=1920x1080')
        
        
        
        driver = webdriver.Chrome(options=options)
        driver = Chrome(options=options)
        
        driver.get(url)
        try:
            time.sleep(3)
            signin = driver.find_element(By.ID, 'header-login-button')
            signin.click()
            time.sleep(4)
            selectbyemailphone = driver.find_element(By.XPATH, "//div[@role='link' and @data-e2e='channel-item']//div[contains(@class, 'css-1cp64nz-DivTextContainer')]//div[text()='Use phone / email / username']")
            time.sleep(3)

            selectbyemailphone.click()
            selectbyemail = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1usm4ad-DivDescription e1521l5b3']/a[contains(@href, '/login/phone-or-email/email')]")))
            selectbyemail.click()
            time.sleep(2)
            userfield = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME, "username"))) 
            creds = open("credentials.txt","r")
            credline = creds.read().split("\n")

            time.sleep(4)
            userfield.send_keys(credline[0].split(",")[1])
            passfield = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'][placeholder='Password']"))) 
            passfield.send_keys(credline[1].split(",")[1])
            button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-e2e='login-button']")))
            button.click()
            time.sleep(30)
            driver.quit()
        except Exception:
            driver.quit()

        
        time.sleep(30)
       