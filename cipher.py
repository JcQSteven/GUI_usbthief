import datetime
import time
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import random
import string
import os
class Cipher:
    def __init__(self,usb_path,save_path):
        self.usb_path=usb_path
        self.save_path=save_path

    def aseFile(self):
        generate=False
        now=datetime.datetime.now()
        record_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        h=MD5.new()
        h.update(str(now))
        key=h.hexdigest()
        iv =''.join(random.sample(string.ascii_letters + string.digits, 16))

        cipher =AES.new(key, AES.MODE_CFB,iv)
        for root, dirs, files in os.walk(self.usb_path):
            for file_name in files:
                file_path=os.path.join(root, file_name)
                if self.checkCipher(file_name):
                    generate=True
                    if len(file_path.split('.'))==2:
                        f = open(file_path, 'rb')
                        f_msg = f.read()

                        x = len(f_msg) % 32
                        if x != 0:
                            f_fixed = f_msg + '0' * (32 - x)
                        else:
                            f_fixed = f_msg
                        cipherText = cipher.encrypt(f_fixed)
                        f_new = open(file_path+'.cipher','wb+')
                        f_new.write(cipherText)
                        f_new.close()
                        f.close()
                        os.remove(file_path)

        if generate:
            self.exportKey(record_time, key, iv)
            return 1
        else:
            return 0
    def exportKey(self,record_time,key,iv):
        print self.save_path
        f=open(self.save_path+record_time+'.ini','w+')
        f.write('[decipher]\nkey='+key+'\niv='+iv)
        f.close()
        pass

    def checkCipher(self,file_name):
        if file_name.split('.')[-1] == 'cipher':
            return 0
        else:
            return 1




