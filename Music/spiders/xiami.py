#coding=utf-8

from scrapy.selector import HtmlXPathSelector as pageParser
from scrapy.spider import BaseSpider
from scrapy.http import Request
from Music.items import SogouItem
import urllib

class SogouSpider(BaseSpider):
    name = 'sogou'
    allowed_domains = ['sogou.com']
    start_urls = [#'http://music.sogou.com/song/newtop_1.html',
                  #'http://music.sogou.com/song/topsong_1.html',
                  'http://music.sogou.com/song/enpop_1.html',
                  #'http://music.sogou.com/song/jkpop_1.html',
                  'http://music.sogou.com/song/webbillboardp_1.html',
                  #'http://music.sogou.com/song/ukp_1.html',
                  ]
    
    def __init__(self):
        pass
        
    def parse(self, response):
        hxs = pageParser(response)
        
        titles = hxs.select('//td[@class="title"]/a/text()').extract()
        artists = hxs.select('//a[@uigs="consume=singer_new"]/text()').extract()
        download_pages = hxs.select('//span[@class="cd3"]/a/@onclick').extract()
        #dates = hxs.select('//div[@class="item-date"]/text()').extract()
        for i in range(0, len(titles)):  
            title = titles[i].replace('\t', '').replace('\n', '').replace('\r', '') #+ ' ' + artists[i]
            artist = artists[i].replace('\t', '').replace('\n', '').replace('\r', '')
            query = title
            query = urllib.urlencode({'query':query}).split('=')[1]
                
            sogou_url = 'http://mp3.sogou.com/music.so?query=' + query + '&class=1&st=&ac=1&pf=mp3&_asf=mp3.sogou.com&_ast=1355460624&p=&w=&interV=&w=02009900'      
            yield Request(sogou_url, callback=self.parse_sogou, meta={'title': self.str_replace(title), 'artist': self.str_replace(artist)})       

    def str_replace(self, str):
        return str.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            
    def parse_sogou(self, response):
        hxs = pageParser(response)
        title = response.meta['title']
        artist = response.meta['artist']
        
        data = ''
        try:
            data = hxs.select('//a[@action="down"]/@onclick').extract()[0]
        except:
            print '[ ' + title + ' NOT FOUND]'
        
        if data != '':
            download_page = 'http://mp3.sogou.com' + data.split("'")[1]
            yield Request(download_page, callback = self.parse_download, meta = {'title': title, 'artist': artist})
            
    
    def parse_download(self, response):
        hxs = pageParser(response)
        title = response.meta['title']
        artist = response.meta['artist']
        
        download_link = ''
        links = hxs.select('//a/@href').extract()
        for link in links:
            if '.mp3' in link:
                download_link = link
                break
        
        if download_link != '':
            item = BillboardItem()
            item['title'] = title
            item['artist'] = artist
            item['download_link'] = download_link
            
            yield item
            #        	#download_page = download_pages[i].split("'")[1]
            #         #yield Request(download_page, headers = {'Host':'mp3.sogou.com', 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1'}, callback = self.parse_download, meta = {'title': title, 'artist': artist})
                    
            
            # def parse_download(self, response):
            #     hxs = pageParser(response)
            #     title = response.meta['title']
            #     artist = response.meta['artist']
                
            #     download_link = ''
            #     links = hxs.select('//a/@href').extract()
            #     for link in links:
            #         if '.mp3' in link:
            #             download_link = link
            #             break
                
            #     if download_link != '':
            #         item = SogouItem()
            #         item['title'] = title
            #         item['download_link'] = download_link
            #         item['artist'] = artist

            #         yield item
        
        
        
        
        
