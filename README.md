# 自动下载邮件附件
根据邮件主题的关键词，自动下载包含关键词的邮件附件

### Step1: 获取应用专用密码
* Gmail

  开启两步验证：https://myaccount.google.com/u/0/signinoptions/two-step-verification/enroll-welcome

  获取密码：https://myaccount.google.com/u/0/apppasswords

<img src="https://user-images.githubusercontent.com/47515808/227979462-e4fa0bd6-7d8f-4c5b-bdfa-74c6463ea265.png" width="0%" />

* QQ

<img src="https://user-images.githubusercontent.com/47515808/227997715-15e53648-4941-42d1-b15a-221b4b3c0c53.png" width="60%" />

### Step2: 修改config.txt中的信息
<img src="https://user-images.githubusercontent.com/47515808/228000087-60f8085e-bf3b-4288-a06d-1124bcfce3d6.png" width="60%" />

### Step3: 下载附件
 ```
 python download.py
 ```
<img src="https://user-images.githubusercontent.com/47515808/227980666-63b24cab-ecec-4348-9b83-114df6a8f70c.png" width="40%" />

Note: 用gmail有时候不稳定，会报这个错误，推荐用国内服务器的邮件接收文件
 ```
TimeoutError: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
 ```
