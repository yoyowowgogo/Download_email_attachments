import os
import poplib
import email
import telnetlib
import time
from email.parser import Parser
from email.header import decode_header
import codecs

def decode_str(s):#字符编码转换
    list=decode_header(s)
    list_len=len(list)
    res=""
    for i in range(list_len):
        value, charset = list[i]
        if charset:
            value = value.decode(charset)
            res=res+value
    # print("res:",res)
    return res

def check_filename_available(filename):
    n=[0]
    def check_meta(file_name):
        file_name_new=file_name
        if os.path.isfile(file_name):
            file_name_new=file_name[:file_name.rfind('.')]+'('+str((n[0]+1))+')'+file_name[file_name.rfind('.'):]
            n[0]+=1
        if os.path.isfile(file_name_new):
            file_name_new=check_meta(file_name)
        return file_name_new
    return_name=check_meta(filename)
    return return_name


def get_att(msg, subjectString,downloadFilePath):
    subject = msg.get("Subject", "")
    print("subject_before:",subject)
    if subject:
        subject = decode_str(subject)
    print("subject:",subject)
    if subjectString not in subject:
        return 
    print("\n邮件主题：", subject)
    attachment_files = []

    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称类型
        contType = part.get_content_type()

        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)  # 对附件名称进行解码
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                print("附件:"+filename)
                # filename = filename.encode("utf-8")
            data = part.get_payload(decode=True)  # 下载附件
            if os.path.isdir(downloadFilePath):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
                pass
            else:
                os.mkdir(downloadFilePath)  ##只能创建单级目录
            filePath=check_filename_available(downloadFilePath+"\\"+ filename)
            att_file = open( filePath, 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            attachment_files.append(filename)
            att_file.write(data)  # 保存附件
            att_file.close()
    return attachment_files


if __name__ == "__main__":
    # 在这里设置config.txt的路径
    configFileName='config.txt'

    text=codecs.open(configFileName, 'r','utf-8')
    config= text.read()
    config= config.splitlines()

    # POP3服务器、用户名、密码、主题词
    host = config[0]  # pop.qq.com
    username = config[1]  # 用户名
    password = config[2]  # 密码
    subjectString=config[3] #邮件主题包含的特定词
    downloadFilePath=config[4] #保存的文件夹

    print("-------------初始化设置如下---------------")

    print("POP3服务器:",host)
    print("用户名:",username)
    print("授权码:",password)
    print("主题词:",subjectString)
    print("下载文件保存路径:",downloadFilePath)
    print("\n开始连接pop服务器")
    # telnetlib.Telnet(host, 995)
    try:
        server = poplib.POP3_SSL(host)
    except:
        time.sleep(5)
        server = poplib.POP3_SSL(host, 995, timeout=10)
    print("连接pop服务器成功")
    # 身份验证
    server.user(username)
    server.pass_(password) # 参数是你的邮箱密码，如果出现poplib.error_proto: b'-ERR login fail'，就用开启POP3服务时拿到的授权码
    print("登陆账号成功")
    # stat()返回邮件数量和占用空间:
    # print('Messages: %s. Size: %s' % server.stat())

    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    resp, mails, octets = server.list()
    # print(mails)
    print("---------开始遍历邮件啦-------")
    print("已下载：")
    # 倒序遍历邮件
    index = len(mails)
    for i in range(index, 0, -1):
        # lines存储了邮件的原始文本的每一行
        resp, lines, octets = server.retr(i)

        # 邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode("utf8", "ignore")

        # 解析邮件:
        msg = Parser().parsestr(msg_content)

        # 获取附件
        f_list = get_att(msg,subjectString,downloadFilePath)

    print("\n文件下载完成")
