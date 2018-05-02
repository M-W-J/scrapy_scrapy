# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
from xiecheng_scrapy.items import XiechengScrapyItem,XiechengComments,XiechengTicket

class XiechengScrapyPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        
        self.db = self.client[settings['MONGO_DB']]  
        self.scenic_comments_coll = self.db[settings['SCENIC_COMMENTS_COLL']] 
        self.scenic_info_coll = self.db[settings['SCENIC_INFO_COLL']]  
        self.scenic_tickes_coll = self.db[settings['SCENIC_TICKES_COLL']] 

    def process_item(self,item ,spider):
        # self.scenic_data = XiechengScrapyItem  
        if isinstance(item, XiechengScrapyItem): 
            self.scenic_info_coll.insert(dict(item))  
        if isinstance(item, XiechengTicket): 
            self.scenic_tickes_coll.insert(dict(item))  
        if isinstance(item, XiechengComments): 
            self.scenic_comments_coll.insert(dict(item))  
        return item 