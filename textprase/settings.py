# -*- coding: utf-8 -*-

# Scrapy settings for textprase project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'textprase'

SPIDER_MODULES = ['textprase.spiders']
NEWSPIDER_MODULE = 'textprase.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'textprase (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'textprase.pipelines.TextprasePipeline':100,}
