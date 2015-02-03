# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 
from textprase.items import TextpraseItem

from scrapy.selector import HtmlXPathSelector

class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com"]
    start_urls = (
        'http://roll.finance.sina.com.cn/finance/gncj/jrxw/index_\d+.shtml',
    )

    rules = [Rule(SgmlLinkExtractor(allow=['finance/gncj/jrxw/index_\d+']), 'parse_torrent')]

    def parse(self, response):
	x = scrapy.Selector(response)
	#hx = TextpraseItem()
	sites = x.xpath('//ul[@class="list_009"]/li')
	items1 = []
	for ct in sites:
		item=TextpraseItem()
		item['title']= ct.xpath('a/text()').extract()
	#	title=[]
	#	for i in item['title']:
	#		i=i.decode('unicode_escape')
	#		title.append(i)
	#	item['title']=title
		item['url'] = ct.xpath('a/@href').extract()
		items=[]
		items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in item['url']]) 
		item['updatetime']=scrapy.Selector(items[0]).xpath('//a')#ct.xpath('span/text()').extract()
		items1.append(item)
	#hx['content']=x.xpath('//*[@id="artibody"]/text()').extract()
	#hx['publishdate']=NUL
        return items1
