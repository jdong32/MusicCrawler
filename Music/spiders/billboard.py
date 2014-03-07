#coding=utf-8

from scrapy.selector import HtmlXPathSelector as pageParser
from scrapy.spider import BaseSpider
from scrapy.http import Request
from Music.items import BillboardItem
import urllib

class BillBoardSpider(BaseSpider):
    name = 'billboard'
    allowed_domains = ['billboard.com', 'sogou.com']
    start_urls = []
    
    def __init__(self):
        self.start_urls.append('http://www.billboard.com/charts/hot-100?begin=21&order=position&decorator=service&confirm=true')
        for i in range(1, 10):
            self.start_urls.append('http://www.billboard.com/charts/hot-100?page='+ str(i) +'&order=position&decorator=service&confirm=true')
        
        
    def parse(self, response):
        hxs = pageParser(response)
        
        #titles = hxs.select('//div[@class="item-title"]/text()').extract()
        #artists = hxs.select('//div[@class="item-artist"]/text()').extract()
        #dates = hxs.select('//div[@class="item-date"]/text()').extract()

        
        nodes = hxs.select('//article[contains(@class, "song_review")]')
        
        for node in nodes:
            title = node.select('./header/h1/text()').extract()[0]
            if_artist = node.select('./header/p[@class="chart_info"]/a/text()').extract()
            
            if len(if_artist) > 0:
                artist = if_artist[0]
            else:
                artist = 'unknown'
 
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
        
        
        
        
        