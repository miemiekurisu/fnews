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
    name = "sinanew"
    allowed_domains = ["sina.com","sina.com.cn"]
    start_urls = (
        'http://roll.finance.sina.com.cn/finance/gncj/jrxw/index_1.shtml',
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
        item['title']= ct.xpath('a/text()').extract()
	item['url'] = ct.xpath('a/@href').extract()
        item['updatetime']=self.timelineparse(ct.xpath('span/text()').extract()[0])
        return item

    def loadcontent(self,ct):
	item = ct.meta['item']
        x = scrapy.Selector(ct)
        item['content']= x.xpath('//*[@id="artibody"]/p/text()').extract() 
	return item


    def parse(self, response):
	x = scrapy.Selector(response)
	#hx = TextpraseItem()
	sites = x.xpath('//ul[@class="list_009"]/li')
	for ct in sites:
            item = self.load_item(ct)
            yield scrapy.Request(item['url'][0],meta={'item':item},callback=self.loadcontent)

        nextpg = x.xpath('//span [@class="pagebox_next"]')
        staticurl = 'http://roll.finance.sina.com.cn/finance/gncj/jrxw/'
        for np in nextpg:
            #print np.xpath('a/@title').extract()
            if np.xpath('a/@title').extract()[0]==u'\u4e0b\u4e00\u9875':
            #    print 'OK' 
            #    print np.xpath('a/@href').extract() 
                nexturl=staticurl+np.xpath('a/@href').extract()[0][1:]
                yield scrapy.Request(nexturl,callback=self.parse)
                break
            else:
                continue
	# items1.append(item)
        #return items1
