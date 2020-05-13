# Automatic_Check_in
上海海事大学健康系统自动打卡

## 实现流程图
```
graph TD
	A(模拟用户教务系统登陆) --> B(记录保存用户Cookie)
	B --> C(服务端调用接口实现模拟打卡)
```

## 目錄結構
├── Readme.md                   // 说明文件
├── src                         // 代码
│   ├── CookieHunter-Thread.py  // 用户Cookie获取
│   ├── dk.py                   // 打卡
│   ├── user.txt                // 用户个人信息
└───└── cookieFile.txt          // 用户Cookie

## 版本更新

### v1.1 109年5月14日
修复请求时可能会崩溃的BUG

### v1.0 109年4月14日
第一个版本发布
