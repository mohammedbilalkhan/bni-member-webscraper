from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import  NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import csv
import pandas as pd
import time, datetime, os

def delay(wait_time = 0):
    time.sleep(3 + wait_time)

# current time
currentDateTime = datetime.datetime.now()
currenthour = currentDateTime.hour
currentminute = currentDateTime.minute
currentday = currentDateTime.day
currentyear = currentDateTime.year
currentmonth = currentDateTime.strftime("%b")

# log path
getpwd = os.getcwd()
gpwd = getpwd.replace('\\','/')
logname = f'/BNI Log/BNI Region Log/{currentday}-{currentmonth}-{currentyear}'
logpath = gpwd + logname
if os.path.exists(logpath):
    print('Log Folder Exists.')  
else :
    os.makedirs(logpath)
    print("Log Folder Created.") 

# chrome_options.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option("prefs", { \
"profile.default_content_setting_values.notifications": 2  # 1:allow, 2:block
})
chrome_options.add_argument("--start-maximized")

# Driver
ser = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=ser, options= chrome_options) 

# bni india url
driver.get('https://bni-india.in/en-IN/advancedchaptersearch')
# driver.get('https://bniamerica.com/en-US/advancedchaptersearch')      # bni america url
delay(2)

regionlist = driver.find_elements(By.XPATH, "//select[@id='regionId']/option")
delay()

filename = f'{logpath}/BNI_region.csv'
# checking if logfile exists 
if os.path.exists(f"{filename}"):
    print('log filename exists. So incrementing filename by 1.')
    expand = 1
    while True:
        expand += 1
        new_file_name = filename.split(".csv")[0] + str(expand) + ".csv"
        if os.path.exists(f"{new_file_name}"):
            continue
        else:
            filename = new_file_name
            break
    print(f"Your Log filename is \'{filename.split('/')[-1]}\'")

with open(f'{filename}', 'w', newline='\n', encoding='utf-8') as fileregion:
    fieldname = ['region']
    writeregion = csv.DictWriter(fileregion, fieldnames=fieldname)
    writeregion.writeheader()
    for region in regionlist:
        regionname = region.text
        writeregion.writerow({'region' : regionname})

print('Finished')
driver.close()
        