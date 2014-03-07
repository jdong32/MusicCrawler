#coding=utf-8

from scrapy.selector import HtmlXPathSelector as pageParser
from scrapy.spider import BaseSpider
from scrapy.http import Request
from Music.items import SogouItem
import httplib, urllib

class ComicsSpider(BaseSpider):
    name = 'comics'
    allowed_domains = ['imanhua.com'] 
    start_urls = []

    def __init__(self, name):
        self.start_urls.append('http://www.imanhua.com/v2/user/search.aspx?key=' + urllib.quote(unicode(name, 'utf-8').encode('gb2312')))
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        print response.body 

if __name__ == '__main__':
    print urllib.quote(u'进击的巨人'.encode('gb2312'))
    print urllib.quote(unicode('进击的巨人', 'utf-8').encode('gb2312'))
    # params = urllib.urlencode({'s': 2, 'key': '进击的巨人'})
    # conn = httplib.HTTPConnection('http://www.imanhua.com:80')
    # conn.request('POST', '/v2/user/search.aspx', params)
    # response = conn.getresponse()
    # print response.read()