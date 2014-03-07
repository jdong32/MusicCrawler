#coding=utf-8

import os, sys
import subprocess
import Queue
import thread
from sock import Sock
import time
import downloader
from downloader import Downloaders as Down

from DJColorfulOutput import DJColorfulOutput as colorful

class MusicMain():
    def __init__(self, num_downloaders):
        self.targets = Queue.Queue()
        self.sock = Sock(self.targets)
        self.downloaders = []
        self.NUM_DOWNLOADERS = num_downloaders

    def run_downloaders(self):
        for i in range(0, self.NUM_DOWNLOADERS):
            td = Down('thread' + str(i), self.targets)
            self.downloaders.append(td)
            self.downloaders[i].start()

    def run_billboard(self):
        #subprocess.call('scrapy crawl billboard', shell=True)
        if len(sys.argv) == 2:
            if sys.argv[1] == 'billboard':
                subprocess.call('scrapy crawl billboard', shell=True)
            elif sys.argv[1] == 'sogou':
                subprocess.call('scrapy crawl sogou', shell=True)
            else:
				colorful.printc('[NO SUCH SPIDER]', 'FAIL')	
        else:
			colorful.printc('[INPUT FORMAT python music spider]', 'WARNING')
            
                
    def sock_setup(self):
        thread.start_new_thread(self.sock.sock_listen, ())
    
    def wait4stop(self):
        for i in range(0, self.NUM_DOWNLOADERS):
            self.downloaders[i].join()
        colorful.printc('[MISSION COMPLETE]', 'OKGREEN') 
        
if __name__ == '__main__':
    NUM_DOWNLOADERS = 10
    
    music = MusicMain(NUM_DOWNLOADERS)
    music.sock_setup()
    time.sleep(2)
    music.run_downloaders()
    music.run_billboard()
    music.wait4stop()
