# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TextprasePipeline(object):
    def __init__(self):  
	self.mfile = open('data.csv','a')

    def process_item(self, item, spider):
        #f = codecs.open('test.csv', 'wb', encoding='utf-8') 
	#line = json.dumps(dict(item)) + '\n'
	#f.write(item['title']+',') 
	if len(item['title'])!=0:
	    text = ''
	    for i in item['title']:
	        text=text+i
	    updatetime=''
	    for j in item['updatetime']:
	        updatetime=updatetime+j
	    text= '"'+str(item['url'])+'",'+'"'+text+","+updatetime+'"\n'
	    if text !='' and text !=' ':
	        self.mfile.write(text)
        return item

    def close_spider(self,spider):
	self.mfile.close()
