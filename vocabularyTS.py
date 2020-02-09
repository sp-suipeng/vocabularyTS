#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
from xml.dom.minidom import parse
import csv
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import re
def getXML():
    # 获取当前文件的绝对路径
    cur_path = os.path.abspath(__file__)
    # 获取当前文件的目录
    now_path = os.path.dirname(cur_path)
    # 拼接xml文件的路径
    con_path = os.path.join(now_path + "/config.xml")
    # 读取xml文件
    domTree = parse(con_path)
    rootNode = domTree.documentElement
    # 获取推送时间
    tstime = rootNode.getElementsByTagName("tstime")[0].childNodes[0].data
    # 获取推送量
    tsnumber = rootNode.getElementsByTagName("tsnumber")[0].childNodes[0].data
    # 获取已推送量
    tscur = rootNode.getElementsByTagName("tscur")[0].childNodes[0].data
    # 获取推送账户
    tscounts = rootNode.getElementsByTagName("tscounts")[0].getElementsByTagName("count")
    counts=[]
    for count in tscounts:
        counts.append(count.childNodes[0].data)
    return [tstime,tsnumber,tscur,counts]
def getTSVocabularies(start,end):
    # 获取当前文件的绝对路径
    cur_path = os.path.abspath(__file__)
    # 获取当前文件的目录
    now_path = os.path.dirname(cur_path)
    csvFileName = os.path.join(now_path+"/va.CSV")
    vocs=[]
    with open(csvFileName, newline='', encoding="gbk") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if int(row[0])>=start and int(row[0])<end:
                vocs.append(row[1]+'\n')
    csvfile.close()
    return vocs

def sendMail(count,text):

    text1=''
    for i in text:
        text1+=i+'\t\n'
    # 第三方 SMTP 服务
    mail_host = "smtp.sohu.com"  # 设置服务器
    #可以直接用我的测试
    mail_user = "sptest123"  # 用户名
    mail_pass = "GFDK8UQET5V9C"  # 口令

    sender = 'sptest123@sohu.com'
    receivers = count  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 这里是文章主题
    message = MIMEText(text1, 'plain', 'gbk')
    message['From'] = Header("单词推送", 'utf-8')
    message['To'] = Header("you", 'utf-8')
    # 这里需要改为爬取主题
    subject = '考研单词推送，今日单词'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException:
        return False
def setXML(tscur):
    # 获取当前文件的绝对路径
    cur_path = os.path.abspath(__file__)
    # 获取当前文件的目录
    now_path = os.path.dirname(cur_path)
    # 拼接xml文件的路径
    con_path = os.path.join(now_path + "/config.xml")
    tmp_config="./config.xml"

    # 读取xml文件
    domTree = parse(con_path)
    rootNode = domTree.documentElement
    # 设置已推送量
    rootNode.getElementsByTagName("tscur")[0].childNodes[0].data=tscur
    fw = open(tmp_config, "w")
    domTree.writexml(fw)
    fw.close()
if __name__=="__main__":
    pattern = re.compile("[0-9]+:[0-9]+:[0-9]+")
    while True:
        s = re.findall(pattern, time.ctime())
        hour=int(s[0].split(':')[0])
        if hour>=6 and hour <=23:
            # 读取配置文件
            [tstime, tsnumber, tscur, counts] = getXML()
            # 获取TS单词
            vocabularies = getTSVocabularies(int(tscur), int(tsnumber) + int(tscur))
            # 发送邮件
            result = sendMail(counts, vocabularies)
            # 设置csv
            setXML(str(int(tsnumber) + int(tscur)))
            print(time.ctime()+':'+str(result))
        else:
            pass
        time.sleep(int(tstime)*3600)
