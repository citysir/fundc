#coding=utf-8
  
from ftplib import FTP  
import os, sys, time
import socket  

class MYFTP:  
    def __init__(self, hostaddr, username, password, remotedir, port=21):  
        self.hostaddr = hostaddr  
        self.username = username  
        self.password = password  
        self.remotedir  = remotedir  
        self.port     = port  
        self.ftp      = FTP()  
        self.file_list = []  

    def __del__(self):  
        self.ftp.close()  

    def login(self):  
        ftp = self.ftp  
        try:   
            timeout = 60  
            socket.setdefaulttimeout(timeout)  
            ftp.set_pasv(True)  
            print '开始连接到 %s' %(self.hostaddr)  
            ftp.connect(self.hostaddr, self.port)  
            print '成功连接到 %s' %(self.hostaddr)  
            print '开始登录到 %s' %(self.hostaddr)  
            ftp.login(self.username, self.password)  
            print '成功登录到 %s' %(self.hostaddr)  
            debug_print(ftp.getwelcome())  
        except Exception:  
            deal_error("连接或登录失败")  
        try:  
            ftp.cwd(self.remotedir)  
        except(Exception):  
            deal_error('切换目录失败')  

    def download_file(self, localfile, remotefile):  
        file_handler = open(localfile, 'wb')  
        self.ftp.retrbinary('RETR %s'%(remotefile), file_handler.write)  
        file_handler.close()  
  
    def download_files(self, localdir='./', remotedir='./'):  
        try:  
            self.ftp.cwd(remotedir)  
        except:  
            debug_print('目录%s不存在，继续...' %remotedir)  
            return  
        if not os.path.isdir(localdir):  
            os.makedirs(localdir)  
        debug_print('切换至目录 %s' %self.ftp.pwd())  
        self.file_list = []  
        self.ftp.dir(self.get_file_list)  
        remotenames = self.file_list  
        for item in remotenames:  
            filetype = item[0]  
            filename = item[1]  
            local = os.path.join(localdir, filename)  
            if filetype == 'd':  
                self.download_files(local, filename)  
            elif filetype == '-':  
                self.download_file(local, filename)  
        self.ftp.cwd('..')  
        debug_print('返回上层目录 %s' %self.ftp.pwd()) 

    def upload_file(self, localfile, remotefile):  
        if not os.path.isfile(localfile):  
            return  
        file_handler = open(localfile, 'rb')  
        self.ftp.storbinary('STOR %s' % remotefile, file_handler)  
        file_handler.close()  
        debug_print('已传送: %s'  % localfile)  

    def upload_files(self, localdir='./', remotedir = './', excludes=[]):  
        if not os.path.isdir(localdir):  
            return  
        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        for item in localnames:  
            if item in excludes:
                continue
            src = os.path.join(localdir, item)
            if os.path.isdir(src):  
                try:
                    self.ftp.mkd(item)  
                except:
                    debug_print('目录已存在 %s' % item)  
                self.upload_files(src, item)  
            else:  
                self.upload_file(src, item)  
        self.ftp.cwd('..')  
  
    def get_file_list(self, line):  
        file_arr = self.get_filename(line)  
        if file_arr[1] not in ['.', '..']:  
            self.file_list.append(file_arr)  
              
    def get_filename(self, line):  
        pos = line.rfind(':')  
        while(line[pos] != ' '):  
            pos += 1  
        while(line[pos] == ' '):  
            pos += 1  
        file_arr = [line[0], line[pos:]]  
        return file_arr  

def debug_print(s):  
    print (s)  

def deal_error(e):  
    timenow  = time.localtime()  
    datenow  = time.strftime('%Y-%m-%d', timenow)
    logstr = '%s 发生错误: %s' %(datenow, e)  
    debug_print(logstr)
    sys.exit()  

if __name__ == '__main__':
    f = MYFTP('115.29.10.228', 'ftp_deploy', 'kVsHOX2q2jA3TlgBPQr9EYDfNV21Bz', '/', 7721)  
    f.login()  
    f.upload_files(os.path.dirname(__file__), '/fundc/', excludes=['.git', '.settings', 'doc'])