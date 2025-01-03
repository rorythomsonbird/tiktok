from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import os

class Upload:
    def login():
        
        url = f"https://www.tiktok.com/" #URL
        options = webdriver.ChromeOptions()
        options = ChromeOptions()
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.204 Safari/537.3')
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
            time.sleep(3)
            return driver
        except Exception:
            driver.quit()
            return "error"
        
    def upload(driver, file):
        try:
            time.sleep(15)
            upload_div = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-1qup28j-DivUpload"))) 
            upload_div.click()
            selectvideo = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-e2e='select_video_button']"))) 
            selectvideo.click() 
            time.sleep(10)
            
            
            if os.path.isfile(file): 
                print("File exists, proceeding to upload") 
                pyautogui.typewrite(file, interval=0.1) 
                time.sleep(4)
                pyautogui.press('enter')
                time.sleep(5) 
                hashtags = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#web-creation-caption-hashtag-button.jsx-1601248207.caption-operation-icon")))
                
                
                time.sleep(3)
                cookie_banner = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tiktok-cookie-banner[locale='en']"))) 
                driver.execute_script("arguments[0].remove();", cookie_banner)

                hashtags.click()
                hashtags.click()
                hashtags.click()
                hashtags.click()
                for i in range(20): 
                    
                    pyautogui.press('backspace') 
                    time.sleep(0.1)

                vidhashes = ["Reddit", "AITA", "AMITHEAHOLE"]
                for i in range(0,len(vidhashes)-1): 
                    hashtags.click()
                    pyautogui.typewrite(vidhashes[i], interval=0.1) 
                    time.sleep(0.1)
                
                 
                pyautogui.typewrite(vidhashes, interval=0.1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #for i in range(len(vidhashes.text)): 
                #    hashtags.send_keys(Keys.BACKSPACE)
                
                #hashtags.send_keys(vidhashes)
                print("here")
                
                #declinecookie = WebDriverWait(driver,10).until(By.CSS_SELECTOR, "button[aria-label='Decline optional cookies']")
                #declinecookie.click()
                
                post = WebDriverWait(driver,10).until(EC.presence_of_element_located(((By.XPATH, "//div[contains(@class, 'Button__content Button__content--shape-default Button__content--size-large Button__content--type-primary Button__content--loading-false') and text()='Post']"))))
                post.click()
                time.sleep(30)

            else:
                print("File not found or invalid file path")

            time.sleep(10)
        except Exception:
            
            print(Exception)
            time.sleep(400)
            #driver.get("https://www.tiktok.com/")
            #Upload.upload(driver,file)

        driver.quit()