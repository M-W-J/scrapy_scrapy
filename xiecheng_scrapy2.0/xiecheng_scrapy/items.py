# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 景点基本信息
class XiechengScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    scenic_id = scrapy.Field()
    scenic_name = scrapy.Field()
    scenic_grade = scrapy.Field()
    scenic_address = scrapy.Field()
    scenic_time = scrapy.Field()
    scenic_score = scrapy.Field()
    scenic_price = scrapy.Field()
    scenic_traffic = scrapy.Field()
    scenic_comments_count = scrapy.Field()
    scenic_feature = scrapy.Field()
    scenic_feature_content = scrapy.Field()
    scenic_img = scrapy.Field()
    scenic_polic = scrapy.Field()

# 门票信息
class XiechengTicket(scrapy.Item):
    ticket_id = scrapy.Field()
    ticket_name = scrapy.Field()
    scenic_type = scrapy.Field()
    scenic_reserve_time = scrapy.Field()
    market_price = scrapy.Field()
    ctrip_price = scrapy.Field()
    ticket_detail = scrapy.Field()
    scenic_promise = scrapy.Field()
    scenic_name = scrapy.Field()
    scenic_id = scrapy.Field()
    ticket_payment = scrapy.Field()

# 景点评论
class XiechengComments(scrapy.Item):
    comment_id = scrapy.Field()
    con = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    grade = scrapy.Field()
    uid = scrapy.Field()
    Reply = scrapy.Field()
    scenic_name = scrapy.Field()
    scenic_id = scrapy.Field()
