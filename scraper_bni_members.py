from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
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

# user data
df0 = pd.read_csv(f'region.csv')
regiondict = df0['Region'].to_list()

# chrome_options.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option("prefs", { \
"profile.default_content_setting_values.notifications": 2  # 1:allow, 2:block
})
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--start-maximized")

# Driver
ser = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=ser, options= chrome_options) 


regionloop = -1
while regionloop in range(regionloop, len(regiondict)):
    regionloop = regionloop + 1
    region = regiondict[regionloop]
    
    driver.get('https://bni-india.in/en-IN/advancedchaptersearch')          # bni india url
    # driver.get('https://bniamerica.com/en-US/advancedchaptersearch')      # bni america
    delay(3)
    region_select = driver.find_element(By.XPATH, "//select[@id='regionId']")
    region_select.send_keys(region)

    driver.execute_script("window.scrollTo(0,1000)")
    find_btn = driver.find_element(By.XPATH, "//button[@id='submit']").click()

    chpt_table_wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='chapterListTable_wrapper']")))

    if os.path.exists(f'{logpath}/{region}'):
        print('Region Directory exists.')
    else:
        os.mkdir(f'{logpath}/{region}')
        print('Region Directory Created.')

    with open(f'{logpath}/{region}/{region}.csv', 'a', newline='\n', encoding='UTF-8') as regionfile:
        regionfield = ['ChapterName', 'ChapterLink']
        regionwriter = csv.DictWriter(regionfile, fieldnames=regionfield)
        regionwriter.writeheader()

        get_chpt_names = driver.find_elements(By.XPATH, "//a[@class='linkone']")
        driver.execute_script("window.scrollTo(0,1000)")
        for chpt_l in get_chpt_names:
            chpt_link = chpt_l.get_attribute('href')     # save the chapter names in a file.
            chpt_n = chpt_l.text
            chpt_n = chpt_n.replace('/', '-')
            regionwriter.writerow({'ChapterName': chpt_n, 'ChapterLink': chpt_link})
        delay()
    regionfile.close()

        # reading region_names
    df = pd.read_csv(f'{logpath}/{region}/{region}.csv')     
    read_chpt_link = df['ChapterLink'].to_dict()
    read_chpt_name = df['ChapterName'].to_dict()
    len_chpt_link = len(read_chpt_link)
    print('\nTotal Chapters:', len_chpt_link)

    if len_chpt_link == 0:
        continue
        
    i = 0
    while i in range(0, len_chpt_link):
        chapterlink= read_chpt_link[i]
        chaptername = read_chpt_name[i]
        print('\n', i + 1)
        print('ChapterName:', chaptername)
        print('ChapterLink:', chapterlink)

        driver.get(chapterlink)
        try:
            rowdetailwait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='rowDetail']")))
        except TimeoutException:
            driver.refresh()
            delay()
            pass

        try:   
            membercountlink = driver.find_element(By.XPATH, "//a[@class='numberLink']").click()
        except NoSuchElementException:
            driver.refresh()
            delay()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='numberLink']")))
            membercountlink = driver.find_element(By.XPATH, "//a[@class='numberLink']").click()
            pass
        except ElementClickInterceptedException:
            pass
        membercount = driver.find_element(By.XPATH, "//a[@class='numberLink']").text
        print('memberCount:', membercount)
        delay(-1)


        with open(f'{logpath}/{region}/{chaptername}_memlinks.csv', 'a', newline='\n', encoding='UTF-8') as chapterfile:
            chapterfield = ['MemberName', 'MemberLink', 'MemberCompany', 'MemberSpeciality', 'MemberCount']
            chapterwriter = csv.DictWriter(chapterfile, fieldnames=chapterfield)
            chapterwriter.writeheader()
            
                # looping if there is one more than one page.
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            try:
                pagecount = driver.find_elements(By.XPATH, "//li[@class='paginate_button ']")
                length_pagecount = len(pagecount)
            except NoSuchElementException:
                length_pagecount = 0
                pass

            page = 0
            while page <= length_pagecount:

                memberlinkpath = driver.find_elements(By.XPATH, "//a[@class='linkone']")
                length_memberlinkpath = len(memberlinkpath)
                membercompanypath = driver.find_elements(By.XPATH, "//tbody//td[2]")
                memberspecialitypath = driver.find_elements(By.XPATH, "//tbody//td[3]")

                x = 0
                while x in range(0, length_memberlinkpath):

                    mem_link = memberlinkpath[x].get_attribute('href')
                    mem_name = memberlinkpath[x].text
                    mem_company = membercompanypath[x].text
                    mem_speciality = memberspecialitypath[x].text

                    delay(-1)
                    chapterwriter.writerow({'MemberName': mem_name, 'MemberLink': mem_link, 'MemberCompany': mem_company, 'MemberSpeciality': mem_speciality})
                    
                    x = x + 1
                
                delay(-1)
                try:
                    next_button = driver.find_element(By.XPATH, "//li[@class='paginate_button next']").click()
                    print('\nButton Clicked.')
                except NoSuchElementException:
                    print('\nNot Clicked.')
                    break
                except ElementClickInterceptedException:
                    driver.execute_script("window.scrollTo(0,800)")
                    next_button = driver.find_element(By.XPATH, "//li[@class='paginate_button next']").click()
                    pass
                
                page = page + 1

            chapterwriter.writerow({'MemberCount': f'TotalMembers-{membercount}'})
        chapterfile.close()

        df1 = pd.read_csv(f'{logpath}/{region}/{chaptername}_memlinks.csv')
        member_l = df1['MemberLink'].to_dict()
        member_name = df1['MemberName'].to_dict()
        length_memlink = len(member_l)

            #
        with open(f'{logpath}/{region}/{chaptername}_MemberDetails.csv', 'w', newline='\n', encoding='UTF-8') as memberfile:
            memberfield = ["Name", 
                            "Company", 
                            "Speciality", 
                            "Phone",
                            "DirectPhone",
                            "Website",
                            "Socials",
                            "ComapanyAddr",
                            "BusinessDetail"]
            memberwriter = csv.DictWriter(memberfile, fieldnames=memberfield)
            memberwriter.writeheader()

            m = 0
            while m in range(0, length_memlink - 1):
                # try:

                memberlink = member_l[m]
                membername = member_name[m]
                print('\nMember:', m + 1)
                print(membername)
                print(memberlink)
                try:
                    driver.get(memberlink)
                    delay()
                    driver.execute_script("window.scrollTo(0,3000)")
                except WebDriverException:
                    pass
                try:

                        # memberName
                    memberName = driver.find_element(By.XPATH, "//div[@class='memberProfileInfo']//h2").text
                    print('memberName:', memberName)

                        # memberCompany
                    memberCompany = driver.find_elements(By.XPATH, "//div[@class='memberProfileInfo']//p")
                    memberCompany = memberCompany[0].text
                    print('memberCompany:', memberCompany)

                        # memberSpeciality
                    memberSpeciality = driver.find_element(By.XPATH, "//div[@class='memberProfileInfo']//h6").text
                    print('membeSpeciality:', memberSpeciality)

                        # memberPhone
                    # moredots = driver.find_element(By.XPATH, "//a[@class='moredots']").click()
                    memberPhone = driver.find_element(By.XPATH, "//div[@class='memberContactDetails']//li[1]/a").get_attribute("href")
                    print('memberPhone:', memberPhone)

                        # memberCompanyAddr
                    memberCompanyAddr = driver.find_element(By.XPATH, "//div[@class='textHolder']//h6").text
                    print('memberCompanyAddress:', memberCompanyAddr)
                    
                    try:
                            # memberWebsite
                        memberWebsite = driver.find_element(By.XPATH, "//div[@class='textHolder']//p/a").get_attribute('href')
                        print('memberWebsite:', memberWebsite)
                    except NoSuchElementException:
                        memberWebsite = 'nan'
                        pass
                    
                    try:
                            #memberBusinessDetail
                        memberBusinessDetail = driver.find_element(By.XPATH, "//section[@class='widgetMemberTxtVideo']//p").text
                        print('memberBusinessDetail:', memberBusinessDetail)
                    except NoSuchElementException:
                        memberBusinessDetail = 'nan'
                        pass

                    try:
                            # memberDirectPhone
                        memberDirectPhone = driver.find_element(By.XPATH, "//div[@class='memberContactDetails']//li[2]/a").get_attribute('href')
                        print('memberDirectPhone:', memberDirectPhone)
                    except NoSuchElementException:
                        memberDirectPhone = 'nan'
                        pass
                    
                    try:
                            # memberSocials
                        memberFacebook = driver.find_element(By.XPATH, "//a[@data-original-title='facebook']").get_attribute('href')    # facebook
                        print('memberFacebook:', memberFacebook)
                    except NoSuchElementException:
                        memberFacebook = 'nan'
                        pass

                    try:
                            # memberInsta
                        memberInsta = driver.find_element(By.XPATH, "//a[@data-original-title='instagram']").get_attribute('href')      # instagram
                        print('memberInsta:', memberInsta)
                    except NoSuchElementException:
                        memberInsta = 'nan'
                        pass

                    try:
                            # memberLinkedin
                        memberLinkedin = driver.find_element(By.XPATH, "//a[@data-original-title='linkedin']").get_attribute('href')    # linkedin
                        print('memberLinekdin:', memberLinkedin)
                    except NoSuchElementException:
                        memberLinkedin = 'nan'
                        pass

                    try:
                            # memberBehance
                        memberBehance = driver.find_element(By.XPATH, "//a[@data-original-title='behance']").get_attribute('href')      # behance
                        print('memberBehance:', memberBehance)
                    except NoSuchElementException:
                        memberBehance = 'nan'
                        pass
                    
                    # memberfile.flush()
                    memberwriter.writerow({'Name': memberName, 
                                            'Company': memberCompany, 
                                            'Speciality': memberSpeciality, 
                                            'Phone': memberPhone,
                                            'DirectPhone': memberDirectPhone,
                                            'Website': memberWebsite,
                                            'Socials': [memberFacebook, memberInsta, memberLinkedin, memberBehance],
                                            'ComapanyAddr': memberCompanyAddr,
                                            'BusinessDetail': memberBusinessDetail})         

                except NoSuchElementException:
                    pass
                except NameError:
                    pass
                
                delay()
                print('\nNEXT')
                print('----------------------------------------------------------------------------------------------------')
                m = m + 1

        memberfile.close()
        print('\nNEXT CHAPTER:')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        delay(-1)
        i = i + 1

    print('\n NEXT REGION')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////')

driver.quit()
print('Finished.')

