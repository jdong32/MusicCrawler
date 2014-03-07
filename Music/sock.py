#coding=utf-8

import socket
import Queue
import sys, os
import thread

from DJColorfulOutput import DJColorfulOutput as colorful

class Sock():
    def __init__(self, queue=''):
        self.addr = ('127.0.0.1', 40047)
        self.download_requests = queue
        
    def sock_listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.addr)
        s.listen(100)
        
        while True:
            conn, addr = s.accept()
            msg = conn.recv(1024).decode('utf-8')
            
            args = msg.split('[*]')
            type = args[0]
            title = args[1]
            download_link = args[2]
            
            if type == 'TERMINATE':
                # print '[CLOSING SOCKET]'
                colorful.printc('[CLOSING SOCKET]', 'WARNING')
                self.download_requests.put((type, title, download_link))
                break
            else:
                self.download_requests.put((type, title, download_link))
            conn.close()
        s.close()
        
        
    def send_msg(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.addr)
        try:
            s.sendall(msg.encode('utf-8'))
        except:
            print sys.exc_info()
        s.close()
           