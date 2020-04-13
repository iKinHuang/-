
import requests
import json
import re
from lxml import etree
import jpush as jpush
import time
#from twilio.rest import Client

#sql系统录入（弃用）
'''
def sqlRun(state):
    conn = pymysql.connect(
        host = "127.0.0.1",
        user = "root",
        password = "root",
        database = "sqltest",
        charset = "utf8"
    )

    date = time.strftime("%Y-%m-%d")
    time = time.strftime("%H:%M:%S")
    cursor = conn.cursor()
    sql = "select * from dk where date='" + date + "'"
    result = cursor.execute(sql)
    if result == 0 :
        if state == 1:
            stateText = "打卡成功"
        else:
            stateText = "打卡失败"
        sql = "insert into dk (date, time, state, lasttime) values ('" + date + "', '" + time + "', '" + stateText + "', '" + time + "')"
        cursor.execute(sql)
        conn.commit()
    else:
        sql = "update dk set lasttime = '" + time + "' where date= '" + date + "'"
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()
'''

#SMS平台api（弃用）
'''
def Notification(isSuccess, serverSuccess):
    if isSuccess:
        alert="上报成功！本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S")
    elif serverSuccess:
        alert="上报失败，请登录服务端检查！"
    else:
        alert="Cookie失效或是其它原因，无法登陆！"
    
    accountSID = 'AC14dafad7b18ceaba9fa0b4786d064010'
    authToken = '7cc8730475cad8316ef1b99415f86437'
    client = Client(accountSID, authToken)
    message = client.messages.create(
        body = alert,
        from_ = '+12059004041',
        to = '+8613817332078'
    )
    print(message.sid)
    exit()
'''

'''
def Notification(isSuccess, serverSuccess, userId):
    fp = open("log", "a+")
    push = _jpush.create_push()
    push.audience = jpush.all_
    if isSuccess:
        push.notification = jpush.notification(alert="用户编号:" + userId + " 本次上报成功！本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
        fp.write("用户编号:" + userId + " 本次上报成功！本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    elif serverSuccess:
        push.notification = jpush.notification(alert="用户编号:" + userId + " 本次上报失败! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
        fp.write("用户编号:" + userId + " 本次上报失败! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    else:
        push.notification = jpush.notification(alert="用户编号:" + userId + " 本次上报失败(Cookie失效)! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
        fp.write("用户编号:" + userId + " 本次上报失败(Cookie失效)! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    fp.write("\n")
    fp.close()
    push.platform = jpush.all_
    try:
        response=push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print ("JPushFailure")
    except:
        print ("Exception")
'''
def Notification(isSuccess, serverSuccess, userId):
    fp = open("log", "a+")
    if isSuccess:
        fp.write("用户编号:" + userId + " 本次上报成功！本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    elif serverSuccess:
        fp.write("用户编号:" + userId + " 本次上报失败! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    else:
        fp.write("用户编号:" + userId + " 本次上报失败(Cookie失效)! 本次上报时间：" + time.strftime("%m月%d日，%H:%M:%S"))
    fp.write("\n")
    fp.close()

def run(c):
    user = c.split(",")
    userId = user[0]
    userCookie = user[1]
    state = 0
    url = 'https://dk.shmtu.edu.cn'
    header={
        'Host':'dk.shmtu.edu.cn',
        'Connection':'close',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        }
    cookies={'connect.sid': userCookie}
    s = requests.Session()
    r = s.get(url,headers=header,cookies=cookies,verify=False)
    params={    #存在大量用户的话需要优化
        'xgh': user[0],
        'lon' : '',
        'lat' : '',
        'region': '1',
        'rylx': '4',
        'status': '0'
    }

    url = 'https://dk.shmtu.edu.cn/checkin'

    resp = requests.post(url, params, cookies=cookies, verify=False)
    print(resp.text)

    html = etree.HTML(resp.text)
    stateText = str(html.xpath('/html/body/div/form/div[1]/label/span[2]/text()'))
    print((stateText.split('/')[1]).split("'")[0])
    state = (stateText.split('/')[1]).split("'")[0]
    if state == " 您已上报":
        Notification(True, True, userId)
        state = 1
    else:
        print("上报失败！")
        Notification(False, True, userId)
        state = 2

if __name__ == "__main__":
    state = 0
    app_key= 'e0b24d83da789110285e5ef5'
    master_secret = '0f5763823479a5229375ecf3'
    requests.packages.urllib3.disable_warnings()
    _jpush = jpush.JPush(app_key, master_secret)
    _jpush.set_logging("DEBUG")
    cookieFile = open("/Users/ikin/Desktop/Python实验/健康系统打卡/cookieFile.txt", "r")
    text = cookieFile.read()
    cookies = text.split("\n")
    for c in cookies:
            try:
                print(c)
                state = run(c)
            except:
                userId = c.split(",")[0]
                Notification(False, False, userId)
                state = 3

