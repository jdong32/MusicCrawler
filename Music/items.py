#coding=utf-8

from scrapy.item import Item, Field

class BillboardItem(Item):
    # define the fields for your item here like:
    # name = Field()
    type = 'billboard'
    title = Field()
    download_link = Field()
    artist = Field()
    
class SogouItem(Item):
    type = 'sogou'
    title = Field()
    download_link = Field()
    artist = Field()
