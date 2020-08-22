#   MODULES
# Web 
from selenium import webdriver

# Timing
import time

# Parsing the HTML
from bs4 import BeautifulSoup

# OS Actions
import os


#   PRE START SEQUENCE
# Starting the driver to get to the webpage
driver = webdriver.Firefox()

# Check if folder 'courses' exists
DIRPATH = './courses'
COURFILE = DIRPATH+'/courseList.txt'
LOGON = DIRPATH+'/loginInfo.txt'

if os.path.isdir(DIRPATH):   
    pass
else:
    os.mkdir('courses')

if os.path.isfile(COURFILE):
    with open(COURFILE) as f:
        courses = f.readlines()
    courses = [x.strip() for x in courses]
else:
    driver.quit()
    raise Exception("A courseList.txt file is needed.")



if os.path.isfile(LOGON):
    with open(LOGON) as f:
        logInfo = f.readlines()
    logInfo = [x.strip() for x in logInfo]
else:
    driver.quit()
    raise Exception("A courseList.txt file is needed.")

#   MAIN FUNCTION

# Getting the page
print("Loading Prado...")
driver.get('https://pradogrado1920.ugr.es/')
print("Done.")


# Navigating the login procedure 
print("Logging in...")
id_box = driver.find_element_by_id('imagenSAML')
id_box.click()

cajaUser = driver.find_element_by_id('username')
cajaUser.send_keys(logInfo[0])

cajaPass = driver.find_element_by_id('password')
cajaPass.send_keys(logInfo[1])

botonLogin = driver.find_element_by_xpath("//input[@value='Login']")
botonLogin.click()
print("Done.")

time.sleep(5)

print("Accessing entries...")
count = 1
for i in courses:
    print(i)
    print(count,"/",len(courses))
    actualCourse = driver.find_element_by_xpath("//h4[contains(text(),'"+i+"')]")
    # fis = driver.find_element_by_xpath("//h4[contains(text(),'ESTADÍSTICA - 1920_msegovia@ugr.es_E')]")
    actualCourse.click()
    print("Done.")
    print("Saving HTML...")
    time.sleep(5)
    body = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[3]/div/section/div/div")
    text = body.get_attribute('innerHTML')

    file_ = open('page'+i+'.html','w')
    file_.write(text)
    file_.close()
    print("Done.")
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    count += 1



print("Task done. Quitting.")
driver.quit()

# exec(open("./webscraperPRADO.py").read())