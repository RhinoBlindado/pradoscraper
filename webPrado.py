#   MODULES
# Web 
from selenium import webdriver

# Timing
import time

# Parsing the HTML
import bs4

# OS Actions
import os

# Differences
import difflib

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
    #body = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[3]/div/section/div/div")
    body = driver.find_element_by_id('region-main')
    #textHTML = body.get_attribute('innerHTML')
    parsedHTML = bs4.BeautifulSoup(body.get_attribute('innerHTML'))
    text = list(parsedHTML.stripped_strings)

    file_ = open('courses/page_'+i+'.txt','w')
    file_.write('\n'.join(text))
    file_.close()
    print("Done.")
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    count += 1


print("Waiting a few secs...")
time.sleep(10)
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
    #body = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[3]/div/section/div/div")
    body = driver.find_element_by_id('region-main')
    #textHTML = body.get_attribute('innerHTML')
    parsedHTML = bs4.BeautifulSoup(body.get_attribute('innerHTML'))
    text = list(parsedHTML.stripped_strings)

    file_ = open('courses/page_'+i+'__2.txt','w')
    file_.write('\n'.join(text))
    file_.close()
    print("Done.")
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    count += 1
    
print("Comparing for changes...")
for i in courses:
    print(i)
    print(count,"/",len(courses))
    txt1=open('courses/page_'+i+'.txt','r').readlines()
    txt2=open('courses/page_'+i+'__2.txt','r').readlines()

    for line in difflib.unified_diff(txt1,txt2):
        print(line)

print("Task done. Quitting.")
driver.quit()

# exec(open("./webscraperPRADO.py").read())