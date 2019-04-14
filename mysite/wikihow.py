
# coding: utf-8

# In[1]:


import scrapy
from urllib.parse import urljoin
import urllib.parse as urlparse


# In[2]:


# Settings for notebook
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# Show Python version
import platform
platform.python_version()


# In[3]:


from scrapy.crawler import CrawlerProcess


# In[4]:


# setup a pipeline 
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('wikihow6.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# In[5]:


# define a spider:
import logging

class InstructablesSpider(scrapy.Spider):
    name = "wiki"
    count=0
    start_urls = ['https://www.wikihow.com/Category:Arts-and-Entertainment', 'https://www.wikihow.com/Category:Cars-%26-Other-Vehicles', 'https://www.wikihow.com/Category:Computers-and-Electronics', 'https://www.wikihow.com/Category:Education-and-Communications', 'https://www.wikihow.com/Category:Family-Life', 'https://www.wikihow.com/Category:Finance-and-Business', 'https://www.wikihow.com/Category:Food-and-Entertaining', 'https://www.wikihow.com/Category:Health', 'https://www.wikihow.com/Category:Hobbies-and-Crafts', 'https://www.wikihow.com/Category:Holidays-and-Traditions', 'https://www.wikihow.com/Category:Home-and-Garden', 'https://www.wikihow.com/Category:Personal-Care-and-Style', 'https://www.wikihow.com/Category:Pets-and-Animals', 'https://www.wikihow.com/Category:Philosophy-and-Religion', 'https://www.wikihow.com/Category:Relationships', 'https://www.wikihow.com/Category:Sports-and-Fitness', 'https://www.wikihow.com/Category:Travel', 'https://www.wikihow.com/Category:WikiHow', 'https://www.wikihow.com/Category:Work-World', 'https://www.wikihow.com/Category:Youth']
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'wikihow6.json'                        # Used for pipeline 2
    }
    
    
    def parse(self, response): # at category page
        paths=response.xpath('//*[@id="cat_all"]/div/a/@href').extract()
        next=response.xpath('//*[@id="cat_all"]/a[@rel="next"]/@href').extract()
        for path in paths: # loop through each project in the category page
            url = urljoin(response.url, path)
            print(url)
            yield scrapy.Request(url, callback=self.parse2)
        print(response)
        if len(next)>0:
            nextpageurl = urljoin(response.url, next[0])
            yield scrapy.Request(nextpageurl, callback=self.parse)

        
            
    def parse2(self, response): # at project page
        try:
            id = response.xpath('//meta[@name="twitter:app:url:iphone"]/@content')[0].extract()[21:]
        except:
            id = None
        
        try:
            v_count=response.xpath('//*[@id="sp_helpful_rating_count"]/text()').get().split()[0]
        except:
            v_count=None
        
        try: 
            rating=response.xpath('//*[@id="sp_helpful_rating_count"]/text()').get().split()[3]
        except:
            rating=None
            
        try: 
            authors=response.xpath('//*[@id="sp_stats_box"]/div[1]/span/text()')[0].extract()
        except:
            authors=None
        
        try:
            category=response.xpath('//*[@id="breadcrumb"]/li[3]/a/text()')[0].extract()
        except:
            category=None
        
        yield {
            'title':response.xpath('//*[@id="intro"]/h1/a/text()')[0].extract(),
            'project_id': id,
            'co_authors': authors,
            'category': category,
            'sub_category':response.xpath('//*[@id="breadcrumb"]/li[4]/a/text()').get(),
            'view_count': response.xpath('//*[@id="sp_stats_box"]/div[3]/span/text()').get(),
            'vote_count': v_count,
            'rating': rating,
            'introduction': response.xpath('//*[@id="intro"]/p[2]/text()').get(),
            'url': response.url,
            'image': response.xpath('/html/head/meta[@property="og:image"]/@content').get(),
            'publish_date': response.xpath('//*[@id="sp_modified"]/span/text()').get()

        }


# In[6]:


# Start the crawler
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(InstructablesSpider)
process.start()

