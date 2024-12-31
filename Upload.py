from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time

class Upload:
    def send_message():
        url = f"https://www.google.com/?zx=1735652103740&no_sw_cr=1" #URL
        options = webdriver.ChromeOptions()
        options = ChromeOptions()
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.204 Safari/537.3')
        options.add_argument('--window-size=1920x1080')
        
        
        
        #options.add_argument('--disable-gpu')
        #options.add_argument('--disable-extensions')
        #options.add_argument('--ignore-ssl-errors=yes')
        #options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)
        driver = Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        #signin = driver.find_element(By.ID, 'menu-button-:r15:')
        #signin.click()
        time.sleep(10)
        time.sleep(90000000000)
        #Get around the focus guard
        # guarddelete = driver.find_element(By.CSS_SELECTOR,"div[data-focus-guard='true'][tabindex='0'][style='width: 1px; height: 0px; padding: 0px; overflow: hidden; position: fixed; top: 1px; left: 1px;'][data-aria-hidden='true'][aria-hidden='true']")
        # driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", guarddelete)
        # time.sleep(6)
        # guarddelete = driver.find_element(By.CSS_SELECTOR,"div.chakra-portal[data-aria-hidden='true'][aria-hidden='true']")
        # driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", guarddelete)
        #email = 
        #email.send_keys("wormywormman2@gmail.com")
        time.sleep(30)
        # textarea = driver.find_element('css selector', 'textarea[data-testid="chat-input-textarea"]')
        # button = driver.find_element('css selector', 'button[aria-label="Send"]')
        # time.sleep(5)
        # email = driver.find_element(By.CSS_SELECTOR,"input.chakra-input.css-z7n099")
        # email.send_keys("wormywormman2@gmail.com")
        # time.sleep(3)
        # emailbutton = driver.find_element(By.CSS_SELECTOR,"button.chakra-button.css-1p10gbu")
        # emailbutton.click()
        # time.sleep(3000)
        # textarea = driver.find_element(By.CSS_SELECTOR, 'textarea[data-testid="chat-input-textarea"]')
        # button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Send"]')

        # textarea.send_keys("Hello")
        # button.click()