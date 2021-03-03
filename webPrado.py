#!/usr/bin/env python3

#   MODULES
# Web 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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

# Database support
import sqlite3
from sqlite3 import Error

#Exception handling
import traceback
import logging

#   FUNCTIONS
def checkStatus():
    '''
    @brief Check if the needed folders exist.
    
    
    @returns    logInfo     The login information.
                courses     List of the courses.
    '''

    DIRPATH = './courses'
    COURFILE = DIRPATH+'/courseList.txt'
    LOGON = DIRPATH+'/loginInfo.txt'

    # Check if folder 'courses' exists.
    if not os.path.isdir(DIRPATH):   
        print("COURSES folder not found, making one.")
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
    '''
    @brief Realize the log in prodecure to Prado
    
    @param logInfo  List containing the email and password for Prado
    
    @param driver   Selenium object to interact with the website.
    '''

    print("Loading Prado...")
    driver.get('https://pradogrado2021.ugr.es/')
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

def courseRead(courses, driver):
    '''
    @brief Read the information in the courses.

    @param courses  String list of the courses to read.

    @param driver   Selenium object to interact with the website.     
    '''

    # Accessing the courses.
    print("Accessing entries...")
    count = 1

    for i in courses:
        print(i)
        print(count,"/",len(courses))

        try:
            actualCourse = driver.find_element_by_xpath("//h4[contains(text(),'"+i+"')]")
        except NoSuchElementException:
            print("Error: Course "+i+" cannot be found!")
        else:
            actualCourse.click()

            print("Done.")
            print("Saving Data...")

            time.sleep(5)
            body = driver.find_element_by_id('region-main')

            # Parse the HTML so it removes all the clutter, only leaves human-readable text.
            parsedHTML = bs4.BeautifulSoup(body.get_attribute('innerHTML'),features="html.parser")
            text = list(parsedHTML.stripped_strings)

            # Check if there's a file already, if there is, save as temp to compare later.
            if os.path.isfile('courses/page_'+i+'.txt'):
                file_ = open('courses/page_'+i+'_temp.txt','w')
            else:
                file_ = open('courses/page_'+i+'.txt','w')
            file_.write('\n'.join(text))
            file_.close()
            driver.execute_script("window.history.go(-1)")

        print("Done.")
        time.sleep(5)
        count += 1


def courseDiff(courses, driver):
    '''
    @brief Check differences between old and new versions of the saved courses.

    @param courses  String list of the courses to read.

    @param driver   Selenium object to interact with the website.

    @return Returns a string object containing the differences between the courses.    
    '''

    print("Comparing for changes...")
    count = 0
    log = ""

    for i in courses:
        print(i)
        print(count+1,"/",len(courses))
        log += ("---- COURSE ["+ str(count+1) + "/" + str(len(courses)) + "]: " + i + "\n")

        # Check that the temp file exists, since if it doesn't it means its the first time running and there's nothing else to compare.
        # And also check that both files are not the same, sice if they're the same, there's no reason to compare them.

        if os.path.isfile('courses/page_'+i+'_temp.txt') and not filecmp.cmp('courses/page_'+i+'.txt','courses/page_'+i+'_temp.txt'):

            try:
                txt1 = open('courses/page_'+i+'.txt','r').readlines()
                txt2 = open('courses/page_'+i+'_temp.txt','r').readlines()
            except FileNotFoundError:
                print("No changes.")
                log += ("\tNo changes.\n")
            else:
                for line in difflib.unified_diff(txt1, txt2, n=0):
                    print(line)
                    log += line 

                os.remove('courses/page_'+i+'.txt')
                os.rename('courses/page_'+i+'_temp.txt','courses/page_'+i+'.txt')

        else:
            print("No changes.")
            log += ("\tNo changes.\n")
            
            if(os.path.isfile('courses/page_'+i+'_temp.txt')):
                os.remove('courses/page_'+i+'_temp.txt')


        log += ("\n\n")
        count += 1
    
    return log

def logPrint(log):

    file = open('log.txt','a')
    theTime = datetime.now()

    file.write(('---------------- CHANGES @ ' + theTime.strftime("%I:%M %p, %A %d/%m/%Y") + ' ---------------- \n'))
    file.write(log + "\n\n")
    file.close()


def getCourseList(driver):
    '''
    Get the courses list from PRADO
    '''

    # Find the drop-down menu
    dropDown = driver.find_element_by_css_selector('li.dropdown:nth-child(1)')

    courseList = dropDown.find_elements_by_class_name('dropdown-item')

    for i in range(1, len(courseList)):
        print(courseList[i].text)


#   MAIN FUNCTION
def main():

    try:
        # Check current status of files.
        logInfo, courses = checkStatus()

        # Start up the driver
        driver = webdriver.Firefox()

        # Login Procedure.
        logIn(logInfo, driver)


        #getCourseList(driver)

        # Read the course list
        courseRead(courses, driver)

        # Compare for changes
        logDiff = courseDiff(courses, driver)

        # Print differences to logfile
        logPrint(logDiff)
        
    except Exception as excpt:
        print("An error ocurred: "+str(excpt))
        traceback.print_exc()
    else:
        # Ending procedure, closing the Selenium browser.
        print("Task done. Quitting.")
    finally:
        driver.quit()



# Setting up the script enviroment
if __name__ == "__main__":
    main()
    

# exec(open("./webPRADO.py").read())