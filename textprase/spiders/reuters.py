# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 
from textprase.items import TextpraseItem
from scrapy.selector import HtmlXPathSelector
import time

class SinanewSpider(scrapy.Spider):
    name = "reuters"
    allowed_domains = ["reuters.com"]
    start_urls = (
            "http://cn.reuters.com/news/archive/CNTopGenNews?view=page&page=1", 
    )
    def timelineparse(self,st):
        t = time.localtime(time.time())
        year = time.strftime('%Y',t)
        updatetime = ''
        if len(st)==14:
            updatetime=year+'/'+st[1:3]+'/'+st[4:6]+'/'+st[-6:-1]
        elif len(st)==19:
            updatetime=st[1:5]+'/'+st[6:8]+'/'+st[9:11]+'/'+st[-6:-1]
        return updatetime

    def load_item(self,ct):
        item=TextpraseItem()
        item['title']= ct.xpath('h2/a/text()').extract()
	item['url'] = ct.xpath('a/@href').extract()
        item['updatetime']=self.timelineparse(ct.xpath('div/span/text()').extract()[0])
        return item

    def loadcontent(self,ct):
	item = ct.meta['item']
        x = scrapy.Selector(ct)
        item['content']= x.xpath('//*[@class="feature"]//text()').extract() 
	return item


    def parse(self, response):
	x = scrapy.Selector(response)
	sites = x.xpath('//*[@class="feature"]/h2')
	for ct in sites:
            item = self.load_item(ct)
            yield scrapy.Request('http://cn.reuters.com/'+item['url'][0],meta={'item':item},callback=self.loadcontent)

        staticurl = 'http://cn.reuters.com/news/archive/CNTopGenNews?date='
        for np in nextpg:
            if np.xpath('a/@title').extract()[0]==u'\u4e0b\u4e00\u9875':
                nexturl=staticurl+np.xpath('a/@href').extract()[0][1:]
                yield scrapy.Request(nexturl,callback=self.parse)
                break
            else:
                continue
