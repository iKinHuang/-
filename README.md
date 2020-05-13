# Automatic_Check_in

上海海事大学健康系统自动打卡



## 实现流程图

~~~gfm
```flow
st=>start: Start
op1=>operation: 通过教务系统登陆学生账户
op2=>operation: 保存记录用户Cookie
op3=>operation: 调用接口模拟用户打卡
e=>end

st->op1->op2->op3->e
```
~~~


## 目錄結構



├── Readme.md                   // 说明文件

├── src                          

│        ├── CookieHunter-Thread.py       // 用户Cookie获取

│        ├── dk.py                                      // 打卡

│        ├── user.txt                                   // 用户个人信息

└──└── cookieFile.txt                         // 用户Cookie



## 版本更新



#### v1.1  109 年 5 月 14 日

修复请求时可能会崩溃的BUG



#### v1.0  109 年 4 月 14 日

第一个版本发布

