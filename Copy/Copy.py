import shutil
import os
import time

class Copy:
    def __init__(self, usb_path, save_path, type):
        self.usb_path = usb_path
        self.save_path = save_path
        self.type = type

    def dirWalker(self):
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        f = open(self.save_path + time.strftime("%m%d%H%M", time.localtime(time.time())) + ".txt", "w")
        for root, dirs, files in os.walk(self.usb_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                f.writelines(file_path + '\n')
                try:
                    if self.extentName(file_name):
                        self.copyFile(file_path)
                except:
                    pass
        f.close()

        return 1
        pass

    def extentName(self, file_name):
        judge_name = file_name.split('.')[-1]
        for extend_name in self.type.split(','):
            if judge_name == extend_name:
                return 1
        return 0
        pass

    def copyFile(self, file_path):
        shutil.copy(file_path, self.save_path)
        pass
