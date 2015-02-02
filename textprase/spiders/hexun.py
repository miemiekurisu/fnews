# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 
from textprase.items import TextpraseItem

from scrapy.selector import HtmlXPathSelector

class HexunSpider(scrapy.Spider):
    name = "hexun"
    allowed_domains = ["hexun.com"]
    start_urls = (
        'http://www.hexun.com/',
    )

    #rules = [Rule(SgmlLinkExtractor(allow=['/2015-01-26/\d+']), 'parse_torrent')]

    def parse(self, response):
	x = scrapy.Selector(response)
	#hx = TextpraseItem()
	sites = x.xpath('//ul[@class="news-list"]/li')
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
		items1.append(item)
	#hx['content']=x.xpath('//*[@id="artibody"]/text()').extract()
	#hx['publishdate']=NUL
        return items1
