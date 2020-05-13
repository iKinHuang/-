import requests
import json
import re
from lxml import etree
import time
import queue
import threading
import urllib3
urllib3.disable_warnings()

class CheckIn(threading.Thread):
    def __init__(self, userName, cookie, region, rylx, status, queue):
        threading.Thread.__init__(self)
        self.userName = userName
        self.cookie = cookie
        self.region = region
        self.rylx = rylx
        self.status = status
        self.queue = queue

    def run(self):
        print("开始尝试打卡，用户编号:" + self.userName)
        isSuccess = TryCheckIn(self.userName, self.cookie, self.region, self.rylx, self.status)
        Notification(isSuccess, self.userName)
        time.sleep(1)
        self.queue.get()
        self.queue.task_done()
        print("线程" + self.userName + "关闭\n")

def TryCheckIn(userName, cookie, region, rylx, status):
    url = 'https://dk.shmtu.edu.cn/checkin'
    #请求头
    header={
        'Host':'dk.shmtu.edu.cn',
        'Connection':'close',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'
    }
    #请求体
    params={
        'xgh': userName,
        'lon' : '',
        'lat' : '',
        'region': region,
        'rylx': rylx,
        'status': status
    }
    cookies={'connect.sid': cookie}
    try:
        session = requests.Session()
        resp = session.post(url, params, cookies=cookies, verify=False)

        html = etree.HTML(resp.text)
        stateText = str(html.xpath('/html/body/div/form/div[1]/label/span[2]/text()'))
        print((stateText.split('/')[1]).split("'")[0])
        state = (stateText.split('/')[1]).split("'")[0]
        if state == " 您已上报" or state == "已打卡":   #通过接口请求返回的网页与正常显示会有区别
            state = 1
        else:
            state = 0
    except:
        state = 0
    session.close()
    return state

def Notification(isSuccess, userName):
    time.sleep(1)   #可能是发起requests太密集导致的问题？
    deviceId = "uK2iwCcbhmcjwbgSn82kwe"
    fp = open("log", "a+")
    if isSuccess:
        title = "上报成功"
        body = "用户编号" + userName + "于" + time.strftime("%m月%d日，%H:%M:%S") + "成功上报。"
        fp.write("用户编号:" + userName + "\t" + "上报时间:" + time.strftime("%H:%M:%S") + "\n")
    else:
        title = "上报失败"
        body = "用户编号" + userName + "上报失败，请前往服务端查看。"
        fp.write("用户编号:" + userName + "\t" + "失败时间:" + time.strftime("%H:%M:%S") + "\n")
    #向客户端发送信息
    url =  "https://api2.day.app:4443/" + deviceId + "/" + title + "/" + body
    print(url)
    try:
        s = requests.Session()
        r = s.get(url)
    except:
        fp.write("推送时遇到了奇怪的问题\n")
    s.close()
    fp.close()

maxThreads = 1

if __name__ == "__main__":
    cookieFile = open("/usr/cookieFile.txt", "r")
    text = cookieFile.read()
    cookieFile.close()
    fp = open("log", "a+")
    fp.write(time.strftime("%m月%d日") + "\n")
    fp.close()
    usersInfo = text.split("\n")
    #最后一行不能是空，会越界
    q = queue.Queue(maxThreads)
    for user in usersInfo:
        userInfo = user.split(",")
        userName = userInfo[0]
        region = userInfo[1]
        rylx = userInfo[2]
        status = userInfo[3]
        cookie = userInfo[4]

        q.put(userName)

        thread = CheckIn(userName, cookie, region, rylx, status, q)
        thread.start()
    q.join()
    print("所有线程结束")