import ConfigParser
import commands
import platform


class Config:
    config = ConfigParser.ConfigParser()

    def __init__(self):
        self.system = platform.system()

    def setConfigPath(self, config_path):
        self.config_path = config_path
        if config_path:
            self.config.readfp(config_path)
            return 1
        else:
            return 0

    def getConfigPath(self):
        try:
            return self.config_path
        except:
            return 0

    def getSystem(self):
        try:
            self.config.items(self.system)
            return 1, self.system
        except:
            return 0, 0

    def getSave(self):
        return self.config.get(self.system, 'save')

    def getUsb(self):
        if self.system == 'Windows':
            result = self.config.get(self.system, 'usb')
            result = commands.getoutput('dir ' + result).read().strip()
            if result != '':
                return 1, result
            else:
                return 0, result

        if self.system == 'Darwin':
            remove_list = ['Macintosh HD', 'BOOTCAMP']
            result_list = commands.getoutput('ls /Volumes/').split('\n')
            for a in remove_list:
                for b in result_list:
                    if a == b:
                        result_list.remove(a)
            try:
                result = result_list.pop()
                return 1, '/Volumes/' + result
            except:
                return 0, 0

    def getType(self):
        return self.config.get(self.system, 'type')

    def getKey(self):
        return self.config.get('decipher','key')
    def getIv(self):
        return self.config.get('decipher','iv')