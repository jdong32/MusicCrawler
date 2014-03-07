#coding=utf-8

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from sock import Sock

from DJColorfulOutput import DJColorfulOutput as colorful

class StopDownloaders(object):

    def __init__(self):
        self.sock = Sock()
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        #log.msg("opened spider %s" % spider.name)
        # print '[START TO CRAWL SONGS]'
        colorful.printc('[START TO CRAWL SONGS]', 'WARNING')

    def spider_closed(self, spider):
        #log.msg("closed spider %s" % spider.name)
        # print '[INFO GATHERING COMPLETE]'
        colorful.printc('[INFO GATHERING COMPLETE]', 'WARNING')
        self.sock.send_msg('TERMINATE[*]--[*]--')
         
