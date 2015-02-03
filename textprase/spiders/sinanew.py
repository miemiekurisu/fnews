# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 
from textprase.items import TextpraseItem
from scrapy.selector import HtmlXPathSelector

class SinanewSpider(scrapy.Spider):
    name = "sinanew"
    allowed_domains = ["sina.com","sina.com.cn"]
    start_urls = (
        'http://roll.finance.sina.com.cn/finance/gncj/jrxw/index_1.shtml',
    )

    def load_item(self,ct):
        item=TextpraseItem()
        item['title']= ct.xpath('a/text()').extract()
	item['url'] = ct.xpath('a/@href').extract()
        return item

    def loadcontent(self,ct):
	item = ct.meta['item']
        x = scrapy.Selector(ct)
        item['content']= x.xpath('//*[@id="artibody"]/a/text()').extract() 
	return item


    def parse(self, response):
	x = scrapy.Selector(response)
	#hx = TextpraseItem()
	sites = x.xpath('//ul[@class="list_009"]/li')
	for ct in sites:
            item = self.load_item(ct)
            yield scrapy.Request(item['url'][0],meta={'item':item},callback=self.loadcontent)

	# items1.append(item)
        #return items1
