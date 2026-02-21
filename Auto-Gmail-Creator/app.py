# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import time
import random
import datetime
import requests
import csv
import string
from fp.fp import FreeProxy
from fake_useragent import UserAgent

# Option for Auto User info generation
AUTO_GENERATE_UERINFO = True
AUTO_GENERATE_NUMBER = 10

# Include Refer URL
INCLUDE_REFER_URL = False

# Time to wait for SELECTORS.(second)
WAIT = 4

# Max Retry to get phone number from sms-activate.org
REQUEST_MAX_TRY = 10

# Your SMS-Activate API key
API_KEY = "8e49fdB90d0209c085dd1df56cedf00e" #9b6b9eb50d0A30---------d9b7495b
COUNTRY_CODE = "175" #i.e, Austrailian country code, See country table in sms-activate. I often use Australian phone number and it works almost always.

sms_activate_url = "https://sms-activate.org/stubs/handler_api.php"
phone_request_params = {
    "api_key":API_KEY,
    "action":"getNumber",
    "country":COUNTRY_CODE, 
    "service":"go",
}

status_param = {
    "api_key":API_KEY,
    "action":"getStatus"
}

SELECTORS = {
    
    "create_account": [
        "//span[contains(text(),'Create account')]",
        "//span[contains(text(),'إنشاء حساب')]",
        "//button[@type='button']" 
    ],
    'for_my_personal_use': [
        "//span[contains(text(),'personal')]",
        "//span[contains(text(),'شخصي')]",
        "//li[@role='menuitem']"
    ], 
    "first_name": "//*[@id='firstName']", 
    "last_name": "//*[@id='lastName']",
    "username": "//*[@id='selectionc1']", 
    "password": "//input[@name='Passwd']",
    "confirm_password": "//input[@name='PasswdAgain']",

    "next": [
            "//span[contains(text(),'Next')]/..",
            "//span[contains(text(),'التالي')]/..",
            "//button[@type='button']",
            "//span[contains(text(),'I agree')]/..",
            "//span[contains(text(),'أوافق')]/.."
    ],
    "phone_number": "//*[@id='phoneNumberId']",
    "code": "//input[@id='code']",
    "acc_phone_number": "//input[@id='phoneNumberId']",
    "acc_day": "//*[@id='day']",
    "acc_year": "//*[@id='year']",
"acc_month": '//*[@id="month"] | //select[@aria-label="الشهر"] | //select[@aria-label="Month"]',
"acc_gender": '//*[@id="gender"] | //select[@aria-label="الجنس"] | //select[@aria-label="Gender"]',
    "username_select": "//li[1][@role='presentation']" 
}
# https://webflow.com/made-in-webflow/fast , I tried to find the fast websites and you can add more.
SITE_LIST = [
    'https://google.com',
    'https://wizardrytechnique.webflow.io/',
    'https://www.rachelbavaresco.com/',
    'https://lightning-bolt.webflow.io/'
]
proxy_list = None
with open("./data/Proxy_DB.csv", 'r') as proxy_list_file:
    proxy_list = csv.reader(proxy_list_file)
    proxy_list = list(proxy_list)

def generatePassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))

def getRandomeUserAgent():
    UAGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14440.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4807.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14467.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4838.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.7.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14455.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4827.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.17 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14436.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4803.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14475.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14471.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14409.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4829.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14395.0.2021) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4765.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.14 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14484.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14450.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4817.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14473.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14324.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.91 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14454.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4824.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14453.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4816.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14447.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4815.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14477.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14476.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.22 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.64 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.93 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.91.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.55 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.23.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.20 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.36.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.36 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.26 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14682.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.16 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.9.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.5 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14574.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4937.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14716.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14268.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.48 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.61.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.37 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.51.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.32 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.56 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.43.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.54 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14505.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4870.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.16.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.25 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.28.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.44 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14543.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4918.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.31.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.19 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14658.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4975.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36'
    ]
    agent = random.choice(UAGENTS)
    return agent

# This method is for chrome driver initialization. You can customize if you want.
def setDriver():
    # 1. download user agent
    user_agent = "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
    print(f"Using Android User-Agent: {user_agent}")

    # 2. set chrome options
    options = ChromeOptions()
    
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    options.add_argument("--remote-allow-origins=*") 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(f"user-agent={user_agent}")

    # 3. initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 4. set window size to mobile view (to bypass google bot detection)
    driver.set_window_size(360, 740) 
    
    return driver

def main():
    driver = None
    user_number = 0
    i = 0

    if(AUTO_GENERATE_UERINFO):
        user_number = AUTO_GENERATE_NUMBER
        print('################ Open First_Name_DB.csv ################')
        try:
            first_name_file = open("./data/First_Name_DB.csv", 'r')
            first_names = csv.reader(first_name_file)
            first_names = list(first_names)
        except:
            print('################ Please check if First_Name_DB.csv exists ################')
            quit()

        print('################ Open Last_Name_DB.csv ################')
        try:
            last_name_file = open("./data/Last_Name_DB.csv", 'r')
            last_names = csv.reader(last_name_file)
            last_names = list(last_names)
        except:
            print('################ Please check if Last_Name_DB.csv exists ################')
            quit()
    else:
        print('################ Open User.csv ################')
        try:
            user_info_file = open("User.csv", 'r')
            user_infos = csv.reader(user_info_file)
            user_infos = list(user_infos)
            user_number = len(user_infos)
        except:
            print('################ Please check if User.csv exists ################')
            quit()

    while True:
        try:
            # Check if the count reach to the maxium users.
            
            if i == user_number:
                break

            i = i + 1
            print('################ User:', i,' ################')
            if AUTO_GENERATE_UERINFO:
                first_name = random.choice(first_names)[0]
                last_name = random.choice(last_names)[0]
                password = generatePassword()
                birthday = str(random.randint(1,12)) + "/" + str(random.randint(1,28)) + "/" +  str(random.randint(1980,1999))
                user_name_manual = ""
                print(first_name + "\t" + last_name + "\t" + password + '\t' + birthday)
            else:
                row = user_infos[i]
                if "Firstname" == row[0]:
                    continue

                first_name = row[0]
                last_name = row[1]
                password = row[2]
                birthday = row[3]
                print(first_name + "\t" + last_name + "\t" + password + '\t' + birthday)
            try:
                user_name_manual = row[4]
            except:
                user_name_manual = ""

            print('################ Initialize Chrome Driver ################')
            driver = setDriver()

            print('################ Random Refer website to bypass Google Bot Detection ################')
            if INCLUDE_REFER_URL:
                random_url = random.choice(SITE_LIST)
                driver.get(random_url)

            # 4 ways to go to account creation page.
            random_int = random.randint(1,4)
            if random_int ==  1:

                print('################ Creat a google account article ################')
                driver.get('https://support.google.com/accounts/answer/27441?hl=en')
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="hcfe-content"]/section/div/div[1]/article/section/div/div[1]/div/div[2]/a[1]'))).click()
                time.sleep(WAIT)
            elif random_int == 2:
                print('################ Go to account page ################')
                driver.get("https://accounts.google.com")

                time.sleep(WAIT)
                
                print('################ Click "Create account" ################')
                for selector in SELECTORS["create_account"]:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                print('################ Click "For my personal use" ################')
                for selector in SELECTORS["for_my_personal_use"]:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

            elif random_int == 3:
                driver.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
                time.sleep(WAIT)
            
            elif random_int == 4:
                driver.get('https://support.google.com/mail/answer/56256?hl=en')
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="hcfe-content"]/section/div/div[1]/article/section/div/div[1]/div/p[1]/a'))).click()
                time.sleep(WAIT)

            username_try = 0

            # if the username exists, it retries REQUEST_MAX_TRY times.
            while username_try < REQUEST_MAX_TRY:
                time.sleep(WAIT*2)

                print('################ 1st step of Creation Wizard. ################')


                print("################ Generate User Try: ", username_try+1, " ################")
                # set the first name.
                print('################ First Name ################')
                first_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['first_name'])))
                first_name_tag.clear()
                time.sleep(WAIT/2)
                print(first_name)
                first_name_tag.send_keys(first_name)

                # set the surname.
                print('################ Last Name ################')
                last_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['last_name'])))
                last_name_tag.clear()
                last_name_tag.send_keys(last_name)

                #click next button
                print('################ "Next" ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                time.sleep(WAIT*2)

                print('################ 2st step of Creation Wizard. ################')
                print('################ Birthday & Gender (Action Mode) ################')
                from selenium.webdriver.common.action_chains import ActionChains
                time.sleep(3) 
                
                # 1. Day
                day_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, SELECTORS['acc_day'])))
                day_field.send_keys(birthday.split('/')[1])
                
                # 2. Month by moving mouse and click (to bypass google bot detection, because google can easily detect if we use send_keys for month selection)
                month_element = driver.find_element(By.XPATH, SELECTORS['acc_month'])
                actions = ActionChains(driver)
                actions.move_to_element(month_element).click().perform() # move mouse to month selection and click
                time.sleep(1)
                # write month num
                actions.send_keys(birthday.split('/')[0]).send_keys(Keys.ENTER).perform()

                # 3. Year
                driver.find_element(By.XPATH, SELECTORS['acc_year']).send_keys(birthday.split('/')[2])

                # 4. Gender by monving mouse and click
                gender_element = driver.find_element(By.XPATH, SELECTORS['acc_gender'])
                actions.move_to_element(gender_element).click().perform()
                time.sleep(1)
                actions.send_keys("M").send_keys(Keys.ENTER).perform()

                # 5. Next by moving mouse and click
                for selector in SELECTORS['next']:
                    try:
                        btn = driver.find_element(By.XPATH, selector)
                        actions.move_to_element(btn).click().perform()
                        break
                    except:
                        continue

                # 5. Click Next Button
                print('################ Click "Next" Button ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, selector))).click()
                        break
                    except:
                        continue
                time.sleep(WAIT*2)

                # set username
                print('################ Set User Name ################')
                if user_name_manual == "":
                    rand_5_digit_num = random.randint(10000,99999)
                    user_name = first_name +"."+ last_name
                    user_name = user_name.lower() + str(rand_5_digit_num)
                else:
                    user_name = user_name_manual
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['username_select']))).click()
                except:
                    pass
                try:
                    user_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['username'])))
                    user_name_tag.clear()
                    print(user_name)
                    time.sleep(WAIT/2)
                    user_name_tag.send_keys(user_name)
                # time.sleep(WAIT*1000)
                except:
                    pass

                #click next button
                print('################ Click "Next" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                time.sleep(WAIT*2)
                print('################ Check Username Validation ################')
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['username_warning'])))
                    user_name_manual = ""
                    print("Invalid")
                    username_try = username_try + 1
                    continue
                except:
                    print("Valid")
                    pass

                # set password
                print('################ Set Password ################')
                passwd_tag =WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['password'])))
                passwd_tag.clear()
                passwd_tag.send_keys(password)

                print('################ Set Confirm Password ################')
                confirmwd_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['confirm_password'])))
                confirmwd_tag.clear()
                confirmwd_tag.send_keys(password)

                #click next button
                print('################ Click "Next" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                time.sleep(WAIT*2)

                print('################ Check Phone Verification ################')
                without_verification = False
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_day'])))
                    without_verification = True
                    print("No. It doesn't require.")
                    break
                except:
                    print("Yes. It requires")
                    pass
                print('################ Input Phone Number ################')
                try:
                    phone_number_input = WebDriverWait(driver, WAIT*3).until(EC.presence_of_element_located((By.XPATH, SELECTORS['phone_number'])))
                    time.sleep(WAIT)
                    break
                except:
                    username_try = username_try + 1
            number = ""
            activationId = ""
            count = 0
            if without_verification == False:
                print('################ Get Phone Number from SMS_Activate ################')
                while(count < REQUEST_MAX_TRY):
                    res = requests.get(url=sms_activate_url,params = phone_request_params)
                    data = res.text
                    print(data)
                    if "ACCESS_NUMBER" in data:
                        activationId = data.split(':')[1]
                        number = data.split(':')[2]
                        
                        number = '+'+ number
                        print(number)
                        break
                    if "NO_BALANCE" in data:
                        print("Check your Balance in sms-activate.")
                        exit()
                    count = count+1
                    time.sleep(WAIT)
                if number == '':
                    print("################ Cannot get phone number: ", REQUEST_MAX_TRY, " times retrial. ################")
                    raise Exception("Go to next account.")
                
                phone_number_input.send_keys(number)

                #click next button
                print('################ Click "Next" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

                print('################ Get SMS Code from SMS_Activate ################')
                time.sleep(WAIT)

                count_status = 0
                code = ''
                while(True):
                # while(count_status < REQUEST_MAX_TRY):
                    status_param['id'] = activationId
                    print(status_param)
                    res_code = requests.get(url=sms_activate_url,params = status_param)
                    data_code = res_code.text
                    print(data_code)
                    if "STATUS_OK" in data_code:
                        code = data_code.split(':')[1]
                        break

                    count_status = count_status + 1
                    time.sleep(WAIT*5)

                if code == '':
                    print('Cannot receive code from sms_activate: ',REQUEST_MAX_TRY, " times retrial")
                    raise Exception("Go to next account.")

                print('################ Verify Phone Code ################')  
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['code']))).send_keys(code)

                #click next button
                print('################ Click "Verify" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

            time.sleep(WAIT*2)
            print('################ Clear Account Phone Number ################')
            # WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_phone_number']))).clear()

            # print('################ Account Birthday ################')
            # # Date   
            # WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_day']))).send_keys(birthday.split('/')[1])
            
            # # Month
            # select_acc_month = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_month'])))

            # acc_month = Select(select_acc_month)
            # acc_month.select_by_value(birthday.split('/')[0])

            # # Year
            # WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_year']))).send_keys(birthday.split('/')[2])

            # select_acc_gender = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_gender'])))

            # # Gender
            # acc_gender = Select(select_acc_gender)
            # acc_gender.select_by_value('1')

            print('################ Click "Next" Buton ################')
            for selector in SELECTORS['next']:
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                    break
                except:
                    pass
            print('################ Click "I agree" Buton ################')
            time.sleep(WAIT)

            # Scroll to click "I agree"
            driver.execute_script("window.scrollTo(0, 800)") 
            time.sleep(WAIT)
            for selector in SELECTORS['next']:
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                    break
                except:
                    pass
            time.sleep(WAIT*3)
            print('################ Save to Created.txt ################')
            f = open('Created.txt', 'a')
            f.write(user_name + "\t" + password + "\t" +birthday + "\t"+ number + "\n")
            f.close()

            driver.quit()
        except Exception as e:
            print(e)
            if driver is not None:
                driver.quit()

    user_info_file.close()
main()