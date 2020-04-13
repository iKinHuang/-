from selenium import webdriver
import json


def login(user):
    url = 'https://dk.shmtu.edu.cn'
    browser = webdriver.Chrome()
    browser.get(url)
    userLoginInfo = user.split(",")
    userName = userLoginInfo[0]
    password = userLoginInfo[1]
    try:
        browser.find_element_by_xpath('//*[@id="username"]').click()
        browser.find_element_by_xpath('//*[@id="username"]').clear()
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(userName)
        browser.find_element_by_xpath('//*[@id="password"]').click()
        browser.find_element_by_xpath('//*[@id="password"]').clear()
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        browser.find_element_by_xpath('//*[@id="validateCode"]').click()
        validteCode = input()    #预留OCR
        browser.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validteCode)
        browser.find_element_by_xpath('//*[@id="fm1"]/input[4]').click()
        info = browser.find_element_by_xpath('/html/body/div[1]/form/div[1]/label/span[2]')
        if((info.text == "已打卡") or (info.text == "未打卡")): 
            cookie = browser.get_cookies()
            cookieFile = open("cookieFile.txt", "a+")
            cookieFile.write(cookie[0]['value'])    #保存cookie
            cookieFile.write("\n")
            cookieFile.close()
            isSuccess = 1
            browser.quit()
        else:
            isSuccess = 0
            browser.quit()
        
    except:
        isSuccess = 0
        browser.quit()
    return isSuccess


if __name__ == "__main__":
    fp = open("user.txt", "r")
    text = fp.read()
    usersInfo = text.split("\n")   #带有用户信息的列表
    fp.close()
    for user in usersInfo:
        isSuccess = login(user)
        while(not isSuccess):
            isSuccess = login(user)
