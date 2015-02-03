from scrapy.spider import Spider
from scrapy.selector import Selector

#from dirbot.items import Article
from textprase.items import TextpraseItem
import json
import re
import string
from scrapy.http import Request

class YouyousuiyueSpider(Spider):
    name = "youyousuiyue2"
    allowed_domains = ["youyousuiyue.sinaapp.com"]
    
    start_urls = [
        'http://youyousuiyue.sinaapp.com',
    ]
        
    def load_item(self, d):
        item = TextpraseItem()
        title = d.xpath('header/h1/a')
        item['title'] = title.xpath('text()').extract()
        print item['title'][0]
        item['url'] = title.xpath('@href').extract()
        return item

    def parse_item(self, response):
        item = response.meta['item']
        
        sel = Selector(response)
        d = sel.xpath('//div[@class="entry-content"]/div')
        item['content'] = d.xpath('text()').extract()
        return item

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://youyousuiyue.sinaapp.com
        @scrapes name
        """
        
        print 'parsing ', response.url
        sel = Selector(response)
        articles = sel.xpath('//div[@id="content"]/article')
        for d in articles:
            item = self.load_item(d)
            yield Request(item['url'][0], meta={'item':item}, callback=self.parse_item) # ** or yield item

        sel = Selector(response)
        link = sel.xpath('//div[@class="nav-previous"]/a/@href').extract()[0]
        if link[-1] == '4':
            return
        else:
            print 'yielding ', link
            yield Request(link, callback=self.parse)

