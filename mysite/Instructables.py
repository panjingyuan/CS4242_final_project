
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
        self.file = open('instructables.jl', 'w')

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
    name = "Intructables"
    count=0
    start_urls = [
        "https://www.instructables.com/workshop/woodworking/?offset=0",
        "https://www.instructables.com/technology/arduino/?offset=0",
        "https://www.instructables.com/technology/cnc/?offset=0",
        "https://www.instructables.com/technology/electronics/?offset=0",
        "https://www.instructables.com/workshop/tools/?offset=0",
        "https://www.instructables.com/technology/raspberry-pi/?offset=0",
        "https://www.instructables.com/craft/paper/?offset=0",
        "https://www.instructables.com/workshop/cars/?offset=0",
        "https://www.instructables.com/workshop/metalworking/?offset=0",
        "https://www.instructables.com/workshop/furniture/?offset=0",
        "https://www.instructables.com/technology/science/?offset=0",
        "https://www.instructables.com/home/life-hacks/?offset=0",
        "https://www.instructables.com/craft/art/?offset=0",
        "https://www.instructables.com/technology/computers/?offset=0",
        "https://www.instructables.com/technology/3D-Printing/?offset=0",
        "https://www.instructables.com/home/gardening/?offset=0",
        "https://www.instructables.com/craft/sewing/?offset=0",
        "https://www.instructables.com/outside/camping/?offset=0",
        "https://www.instructables.com/home/pets/?offset=0",
        "https://www.instructables.com/outside/survival/?offset=0",
        "https://www.instructables.com/workshop/repair/?offset=0",
        "https://www.instructables.com/craft/jewelry/?offset=0",
        "https://www.instructables.com/craft/fashion/?offset=0",
        "https://www.instructables.com/technology/leds/?offset=0",
        "https://www.instructables.com/play/toys/?offset=0",
        "https://www.instructables.com/home/decorating/?offset=0",
        "https://www.instructables.com/outside/backyard/?offset=0",
        "https://www.instructables.com/workshop/home-improvement/?offset=0",
        "https://www.instructables.com/craft/knitting-and-crocheting/?offset=0",
        "https://www.instructables.com/home/beauty/?offset=0",
        "https://www.instructables.com/food/bbq-and-grilling/?offset=0",
        "https://www.instructables.com/play/offbeat/?offset=0",
        "https://www.instructables.com/technology/photography/?offset=0",
        "https://www.instructables.com/technology/software/?offset=0",
        "https://www.instructables.com/food/dessert/?offset=0",
        "https://www.instructables.com/play/minecraft/?offset=0",
        "https://www.instructables.com/technology/audio/?offset=0",
        "https://www.instructables.com/home/cleaning/?offset=0",
        "https://www.instructables.com/home/kids/?offset=0",
        "https://www.instructables.com/food/snacks-and-appetizers/?offset=0",
        "https://www.instructables.com/home/health/?offset=0",
        "https://www.instructables.com/play/table-top/?offset=0",
        "https://www.instructables.com/home/reuse/?offset=0",
        "https://www.instructables.com/home/halloween/?offset=0",
        "https://www.instructables.com/play/puzzles/?offset=0",
        "https://www.instructables.com/food/beverages/?offset=0",
        "https://www.instructables.com/food/main-course/?offset=0",
        "https://www.instructables.com/technology/robots/?offset=0",
        "https://www.instructables.com/technology/gadgets/?offset=0",
        "https://www.instructables.com/play/video-games/?offset=0",
        "https://www.instructables.com/home/life-skills/?offset=0",
        "https://www.instructables.com/outside/bikes/?offset=0",
        "https://www.instructables.com/play/music/?offset=0",
        "https://www.instructables.com/workshop/molds-and-casting/?offset=0",
        "https://www.instructables.com/workshop/lighting/?offset=0",
        "https://www.instructables.com/workshop/energy/?offset=0",
        "https://www.instructables.com/home/education/?offset=0",
        "https://www.instructables.com/craft/leather/?offset=0",
        "https://www.instructables.com/home/green/?offset=0",
        "https://www.instructables.com/workshop/pallets/?offset=0"
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'instructables.json'                        # Used for pipeline 2
    }
    
    
    def parse(self, response): # at category page
        paths = response.css('div.cover-info span.title a::attr(href)').getall()
        parsed = urlparse.urlparse(response.url)
        count = int(urlparse.parse_qs(parsed.query)['offset'][0])+59
        nextpath = "?offset=" + str(count)
        for path in paths: # loop through each project in the category page
            url = urljoin(response.url, path)
            yield scrapy.Request(url, callback=self.parse2)
        print(response)
        if nextpath in response.css('div#explore-footer div.pull-right ul li a::attr(href)').getall() and count<=19*59:
            nextpageurl = urljoin(response.url, nextpath)
            yield scrapy.Request(nextpageurl, callback=self.parse)

        
            
    def parse2(self, response): # at project page
        yield {
            'title':response.css('h1.header-title::text').get(),
            'project_id': json.loads(response.css('script#js-page-context::text')[0].extract())["ibleData"]["id"],
            'author':response.css('span.header-byline a[rel="author"]::text').get(),
            'author_id': json.loads(response.css('script#js-page-context::text')[0].extract())["ibleData"]["author"]["id"],
            'category': response.xpath("//meta[@property='category']/@content")[0].extract(),
            'channel':response.css('span.header-byline a.channel::text').get(),
            'view_count': response.css('span.header-stats p.svg-views::text').get(),
            'favourite_count': response.css('span.header-stats p.svg-favorite::text').get(),
            'comment_count': response.css('span.header-stats p.svg-comments::text').get(),
            'raw_text': response.css('div.step-body p::text').getall(),
            'url': response.url,
            'image': response.xpath("//meta[@property='og:image']/@content")[0].extract(),
            'publish_date': json.loads(response.css('script#js-page-context::text')[0].extract())["ibleData"]["publishDate"]

        }


# In[6]:


# Start the crawler
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(InstructablesSpider)
process.start()

