# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import jieba

class TextprasePipeline(object):
    def __init__(self):  
	self.mfile = open('data.csv','a')

    def process_item(self, item, spider):
        #f = codecs.open('test.csv', 'wb', encoding='utf-8') 
	#line = json.dumps(dict(item)) + '\n'
	#f.write(item['title']+',') 
	if len(item['title'])!=0:
	    title = ''
	    for i in item['title']:
	        title = title+i
	    content=''
	    for j in item['content']:
                j=j.replace(u'\n','') 
                j=j.replace(u',','')
	        content=content+j
                    
            #seg_list = jieba.cut(content,cut_all=False)
            #print "Test Seg:","/".join(seg_list)
	    text= '"'+str(item['url'])+'","'+title+'","'+content+'","'+item['updatetime']+'"\n'
	    if text !='' and text !=' ':
	        self.mfile.write(text)
        return item

    def close_spider(self,spider):
	self.mfile.close()
