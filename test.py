import os, ftplib


class FTPlogin:
    HOST = str("192.168.0.102")
    USERNAME = str("promiteus")
    PASS = str("armageddon")
    PORT = 2121


class FTPdata(FTPlogin):
    def __init__(self):
        self.ftp = ftplib.FTP(user=self.USERNAME, passwd=self.PASS)
        self.ftp.connect(host=self.HOST, port=self.PORT)

    def get_welcome(self):
        return self.ftp.getwelcome()

    def mkdir(self, dirname):
        return self.ftp.mkd(dirname)

    def listdir(self):
        return self.ftp.nlst()


ftp = FTPdata()
print(ftp.get_welcome())
ftp.mkdir("fnew")
fldr = ftp.listdir()
print(fldr)


print(os.name)
print(FTPdata())