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

# Compare files
import filecmp

# Human Readable Timestamp
from datetime import datetime


#   FUNCTIONS
#   PRE START SEQUENCE
def checkStatus():
    DIRPATH = './courses'
    COURFILE = DIRPATH+'/courseList.txt'
    LOGON = DIRPATH+'/loginInfo.txt'

    # Check if folder 'courses' exists.
    if os.path.isdir(DIRPATH):   
        pass
    else:
        os.mkdir('courses')

    # Check if there's the course list file.
    if os.path.isfile(COURFILE):
        with open(COURFILE) as f:
            courses = f.readlines()
        courses = [x.strip() for x in courses]
    else:
        raise Exception("A courseList.txt file is needed.")

    # Check if there's the Log In information for PRADO.
    if os.path.isfile(LOGON):
        with open(LOGON) as f:
            logInfo = f.readlines()
        logInfo = [x.strip() for x in logInfo]
    else:
        raise Exception("A loginInfo.txt file is needed.")

    
    # Return relevant information to main.
    return logInfo, courses


def logIn(logInfo, driver):
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

#   MAIN FUNCTION
# Check current status of files.
logInfo, courses = checkStatus()

# Start up the driver
driver = webdriver.Firefox()

# Login Procedure.
logIn(logInfo, driver)

# Accessing the courses.
print("Accessing entries...")
count = 1

for i in courses:
    print(i)
    print(count,"/",len(courses))

    actualCourse = driver.find_element_by_xpath("//h4[contains(text(),'"+i+"')]")
    actualCourse.click()

    print("Done.")
    print("Saving Data...")

    time.sleep(5)
    body = driver.find_element_by_id('region-main')
    parsedHTML = bs4.BeautifulSoup(body.get_attribute('innerHTML'),features="html.parser")
    text = list(parsedHTML.stripped_strings)
    file_ = open('courses/page_'+i+'_temp.txt','w')
    file_.write('\n'.join(text))
    file_.close()
    print("Done.")
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    count += 1

print("Comparing for changes...")
count = 0
for i in courses:
    print(i)
    print(count+1,"/",len(courses))

    if not filecmp.cmp('courses/page_'+i+'.txt','courses/page_'+i+'_temp.txt'):

        txt1=open('courses/page_'+i+'.txt','r').readlines()
        txt2=open('courses/page_'+i+'_temp.txt','r').readlines()

        timeObj = datetime.now()
        log = 'Changes in course '+i+' at '+str(timeObj)+'\n\n'

        for line in difflib.unified_diff(txt1,txt2,n=0):
            print(line)
            log += line 

        log_ = open('log.txt','w')
        log_.write(log)
        log_.close()

        os.remove('courses/page_'+i+'.txt')
        os.rename('courses/page_'+i+'_temp.txt','courses/page_'+i+'.txt')

    else:
        print("No changes.")
        os.remove('courses/page_'+i+'_temp.txt')

    count += 1

print("Task done. Quitting.")
driver.quit()

# exec(open("./webPRADO.py").read())
