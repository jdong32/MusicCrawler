#coding=utf-8

import sys, os
import threading
import urllib2
import eyed3

from DJColorfulOutput import DJColorfulOutput as colorful

class Downloaders(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.download_requests = queue
           
    def run(self):
        while True:
            if self.download_requests.empty() is False:
                request = self.download_requests.get()
                type = request[0]
                title = request[1]
                download_link = request[2]
                
                if type == 'TERMINATE':
                    self.download_requests.put(('TERMINATE', '--', '--'))
                    break
                else:     
                    for i in range(0, 2):
                        try:
                            self.download_file(title, download_link)
                            break
                        except:
                            # print '[OOPS BAD LINK]'
                            colorful.printc('[OOPS BAD LINK]', 'FAIL')

    
    def download_file(self, title, download_link):
        wmafile = urllib2.urlopen(download_link)
        # print '[DOWNLOADING ' + title + ' ]'
        colorful.printc('[DOWNLOADING ' + title + ' ]', 'OKBLUE')
        output = open('music/' + title + '.mp3','wb')
        output.write(wmafile.read())
        output.close()         
