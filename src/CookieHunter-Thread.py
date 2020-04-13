from selenium import webdriver
import json
import queue
import threading
import time


class CookieHunter(threading.Thread):
    #构造函数
    def __init__(self, userName, password, queue):
        threading.Thread.__init__(self)
        self.userName = userName
        self.password = password
        self.queue = queue
    
    def run(self):
        print("开启线程，尝试登陆" + self.userName + "\n")
        isSuccess = login(self.userName, self.password)
        while(not isSuccess):
            isSuccess = login(self.userName, self.password)
        self.queue.get()
        self.queue.task_done()
        print("线程" + self.userName + "关闭\n")

def login(userName, password):
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
        print(userName + "的验证码：")
        validteCode = input()    #预留OCR
        browser.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validteCode)
        browser.find_element_by_xpath('//*[@id="fm1"]/input[4]').click()
        info = browser.find_element_by_xpath('/html/body/div[1]/form/div[1]/label/span[2]')
        if((info.text == "已打卡") or (info.text == "未打卡")): 
            cookie = browser.get_cookies()
            cookieFile = open("cookieFile.txt", "a+")
            cookieFile.write(userName + ",")
            cookieFile.write(cookie[0]['value'])    #保存cookie    #修改为sql语句封装
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


maxThreads = 1  #只能同时并发两个线程
#存在问题：同时创建的进程是无法登陆多个账号的（IP限制？）
#破案：密码错了

if __name__ == "__main__":
    fp = open("user.txt", "r")
    text = fp.read()
    usersInfo = text.split("\n")   #带有用户信息的列表

    q = queue.Queue(maxThreads)

    for user in usersInfo:
        userInfo = user.split(",")
        userName = userInfo[0]
        password = userInfo[1]
        q.put(userName)
        thread = CookieHunter(userName, password, q)
        thread.start()
    q.join()
    print("所有线程结束")