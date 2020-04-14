from selenium import webdriver
import json
import queue
import threading
import time
import os
import sys


class CookieHunter(threading.Thread):
    def __init__(self, userName, password, region, rylx, status, queue):
        threading.Thread.__init__(self)
        self.userName = userName
        self.password = password
        self.region = region
        self.rylx = rylx
        self.status = status
        self.queue = queue
    
    def run(self):
        print("开启线程，尝试登陆" + self.userName + "\n")
        isSuccess = login(self.userName, self.password, self.region, self.rylx, self.status)
        #登陆失败再次登陆
        while(not isSuccess):
            print("登陆失败，再次尝试登陆" + self.userName + "\n")
            isSuccess = login(self.userName, self.password, self.region, self.rylx, self.status)
        self.queue.get()
        self.queue.task_done()
        print("线程" + self.userName + "关闭\n")

def login(userName, password, region, rylx, status):
    url = 'https://dk.shmtu.edu.cn'
    browser = webdriver.Chrome()
    browser.get(url)
    try:
        browser.find_element_by_xpath('//*[@id="username"]').click()
        browser.find_element_by_xpath('//*[@id="username"]').clear()
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(userName)
        browser.find_element_by_xpath('//*[@id="password"]').click()
        browser.find_element_by_xpath('//*[@id="password"]').clear()
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        browser.find_element_by_xpath('//*[@id="validateCode"]').click()
        #print(userName + "的验证码：")
        validteCode = input()    #预留OCR
        browser.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validteCode)
        browser.find_element_by_xpath('//*[@id="fm1"]/input[4]').click()
        info = browser.find_element_by_xpath('/html/body/div[1]/form/div[1]/label/span[2]')
        if((info.text == "已打卡") or (info.text == "还未打卡")): 
            cookie = browser.get_cookies()
            print(cookie[0]['value'])
             #未来修改为sql语句封装
            cookieFile = open("/Users/ikin/Desktop/Python实验/健康系统打卡/cookieFile.txt", "a+")
            cookieFile.write(userName + "," + region + "," + rylx + "," + status + ",")
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


maxThreads = 2  #只能同时并发两个线程

#存在问题：同时创建的进程是无法登陆多个账号的（IP限制？）
#破案：密码错了

if __name__ == "__main__":
    fp = open("/Users/ikin/Desktop/Python实验/健康系统打卡/user.txt", "r")
    text = fp.read()
    fp.close()
    usersInfo = text.split("\n")   #带有用户信息的列表

    q = queue.Queue(maxThreads)

    for user in usersInfo:
        userInfo = user.split(",")
        userName = userInfo[0]
        password = userInfo[1]
        region = userInfo[2]  #所在地区
        rylx = userInfo[3]   #接触史
        status = userInfo[4]  #状况
        #print(userInfo)
        q.put(userName)
        thread = CookieHunter(userName, password, region, rylx, status, q)
        thread.start()
    q.join()
    print("所有线程结束")