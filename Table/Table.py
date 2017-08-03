# -*- coding: utf-8 -*-
# Author: Steven
# !/usr/bin/python
import platform
from Tkinter import *
import tkFileDialog
from readConfig import *
from Copy.Copy import *
from cipher import *
from decipher import *

config=Config()

class Table():
    @classmethod
    def __init__(self):
        self.bord = Tk()

    # init部分
    def initTable(self):
        self.bord.title('Usb-Thief')
        self.bord.geometry('350x375+400+300')
        self.bord['bg'] = 'grey'
        self.bord.resizable(False, False)
        self.initWidget()
        self.bord.mainloop()

        pass

    def initWidget(self):
        self.b1 = Button(self.bord, text='导入', width=5,command=lambda :self.importConfig())
        self.b2 = Button(self.bord, text='抓取', width=5,command=lambda :self.startCopy())
        self.b3 = Button(self.bord, text='加密', width=5,command=lambda :self.startCipher())
        self.b4 = Button(self.bord, text='解密', width=5,command=lambda :self.startDecipher())

        self.t1 = Text(self.bord, width=20)  # 信息框
        self.t2 = Entry(self.bord, width=15)  # 系统
        self.t3 = Entry(self.bord, width=15)  # 存储
        self.t4 = Entry(self.bord, width=15)  # u盘
        self.t5 = Entry(self.bord, width=15)  # 类型

        self.l1 = Label(self.bord, text='系统')
        self.l2 = Label(self.bord, text='存储')
        self.l3 = Label(self.bord, text='U盘')
        self.l4 = Label(self.bord, text='类型')

        self.b1.place(x=150, y=150)
        self.b2.place(x=150, y=200)
        self.b3.place(x=150, y=250)
        self.b4.place(x=150, y=300)

        self.t1.place(x=0, y=0)
        self.t2.place(x=190, y=10)
        self.t3.place(x=190, y=40)
        self.t4.place(x=190, y=70)
        self.t5.place(x=190, y=100)

        self.l1.place(x=150, y=12)
        self.l2.place(x=150, y=42)
        self.l3.place(x=150, y=72)
        self.l4.place(x=150, y=102)

    def importConfig(self):
        if config.setConfigPath(self.setPath())and config.getSystem()[0]:
            self.setUsb(config.getUsb()[0],config.getUsb()[1])
            self.setType(config.getType())
            self.setSystem(config.getSystem()[1])
            self.setSave(config.getSave())
        else:
            self.setMsg('[!]错误配置或不存在配置文件\n')
    def startCopy(self):
        if (config.getConfigPath() and config.getUsb()[0]):
            self.setMsg('[*]开始抓取数据\n')
            copy=Copy(config.getUsb()[1],config.getSave(),config.getType())
            if copy.dirWalker():
                self.setMsg('[*]抓取完成\n')
        else:
            self.setMsg('[!]没有导入配置文件\n')
        pass

    def startCipher(self):
        if (config.getConfigPath() and config.getUsb()[0]):
            cipher=Cipher(config.getUsb()[1],config.getSave())
            if cipher.aseFile():
                self.setMsg('[*]文件加密结束\n')
            else:
                self.setMsg('[!]没有文件需要加密\n')
        else:
            self.setMsg('[!]没有导入配置文件\n')
        pass

    def startDecipher(self):
        decipher_dir=self.setFolder()
        if config.setConfigPath(self.setPath()):
            self.setMsg('[*]解密路径为' + decipher_dir + '\n')
            self.setMsg('[*]设置key文件成功\n')
            decipher=Decipher(decipher_dir,config.getKey(),config.getIv())
            if decipher.decipher():
                self.setMsg('[*]解密成功，请查看\n')
            else:
                self.setMsg('[!]没有需要解密的文件\n')
        else:
            self.setMsg('[!]请配置文件！\n')


        pass
    def setFolder(self):
        path=tkFileDialog.askdirectory()
        return path

    def setPath(self):
        path=tkFileDialog.askopenfile(filetypes=[('Initialization File', '.ini')])
        return path

    def setSystem(self, system):
        self.t2.insert(END, system)
        pass

    def setSave(self, save):
        self.t3.insert(END, save)
        pass

    def setType(self, type):
        self.t5.insert(END, type)
        pass

    def setUsb(self,flag,usb):
        if flag:
            self.t4.insert(END, usb)
            self.setMsg('[*]配置初始化完成\n')
        else:
            self.setMsg('[!]USB不存在或无法读取\n')
        pass

    def setMsg(self, msg):
        self.t1.insert(END, msg)
        pass
