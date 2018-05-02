# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
import jsonpath
import time
from xiecheng_scrapy.items import XiechengScrapyItem ,XiechengTicket,XiechengComments


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['www.ctrip.com','piao.ctrip.com']
    start_urls = ['http://piao.ctrip.com/dest/u-_d6_d0_b9_fa/s-tickets/P1/']

    # 生成网页url列表
    def parse(self, response):
         # 获取网页总页数
        pages_count = response.xpath('//span[@class="c_page2_numtop"]/text()').extract()[0].strip().split('/')[1].split('页')[0]
        pages_url = []
        # 景点网页url列表
        for page in range(1,int(pages_count)+1):
        # for page in range(1,3):
            page_url = 'http://piao.ctrip.com/dest/u-_d6_d0_b9_fa/s-tickets/P' + str(page)
            pages_url.append(page_url)
        # print(pages_url)
        for url in pages_url:
            yield scrapy.Request(url=url,callback=self.parse_info)

    # 获取景点url列表
    def parse_info(self,response):
        scenic_href = response.xpath('//a[@class="title"]/@href').extract()
        # print(scenic_href)
        scenic_list = []
        # with open('html.html','w',encoding='utf-8') as fp:
        #     fp.write(response.text)
        for href in scenic_href:
            scenic_url = 'http://piao.ctrip.com' + href
            scenic_list.append(scenic_url)
        # print(scenic_list)
        for url in scenic_list:
            yield scrapy.Request(url=url,callback=self.scenic_info,meta={'url':url})

    # 获取景点及其门票的信息
    def scenic_info(self,response):
         # 景点产品id
        product_id = re.findall(r'productid:(.*),.*',response.text)[0].strip()
        print('product_id:',product_id)
        # 景点id
        url = response.meta['url']
        scenic_id = re.findall(r'.*\/t(\d+)',url)[0]
        print('scenic_id:',scenic_id)
        scenic_information = XiechengScrapyItem()
        # 景点基本信息抓取
        scenic_name = response.xpath('//div[@class="media-right"]/h2[@class="media-title"]/text()').extract_first()
        # print('scenic_name',scenic_name)
        scenic_information['scenic_name'] = scenic_name
        scenic_information['scenic_id'] = scenic_id
        # 景点等级
        scenic_grade = response.xpath('//div[@class="media-right"]/span[@class="media-grade"]/strong/text()').extract_first()
        scenic_information['scenic_grade'] = scenic_grade
        # 景点地址
        scenic_address = response.xpath('//div[@class="media-right"]/ul/li[@style=""]/span/text()').extract_first().strip()
        scenic_information['scenic_address'] = scenic_address
        # 景点开放时间
        scenic_time = response.xpath('//div[@class="media-right"]/ul/li[@class="time"]/span[@class="j-limit"]/text()').extract_first()
        scenic_information['scenic_time'] = scenic_time
        # 景点评分
        scenic_score = response.xpath('//div[@class="grade"]/i/text()').extract_first() + '/5分'
        scenic_information['scenic_score'] = scenic_score
        # 景点价格
        scenic_price = response.xpath('//div[@class="media-price"]/div/span/text()').extract_first().strip()
        scenic_information['scenic_price'] = scenic_price
        # 景点交通
        scenic_traffic = response.xpath('//div[@class="feature-traffic"]')   #修改
        scenic_information['scenic_traffic'] = scenic_traffic.xpath('string(.)').extract_first().strip()
        # 景点评论数
        sceinc_comments_count = response.xpath('//div[@class="grade"]/a/text()').extract_first().split('看')[1].split('点')[0]
        scenic_information['scenic_comments_count'] = sceinc_comments_count
        # 景点政策
        scenic_polic = response.xpath('//dl[@class="c-wrapper-info"]/dd[@style=""]/div[2]/text()').extract_first().strip()
        scenic_information['scenic_polic'] = scenic_polic
        # 景区特色
        scenic_feature = response.xpath('//div[@class="feature-wrapper"]/ul/li/p/text()').extract()
        scenic_information['scenic_feature'] = scenic_feature
        # 景区简介
        scenic_feature_content = response.xpath('//div[@class="feature-content"]/p/text()').extract()[0]
        scenic_information['scenic_feature_content'] = scenic_feature_content
        # 景区图片
        scenic_img = response.xpath('//div[@class="feature-content"]/p/img/@data-src').extract()
        scenic_information['scenic_img'] = scenic_img
        # print('景点基本信息：', scenic_information)
        # 景点信息写入
        print('开始写入景点信息')
        yield scenic_information

        #评论链接
        # for i in range(1,952):
        for i in range(1,100):
            # print('评论抓取')
            commnet_url = 'http://piao.ctrip.com/Thingstodo-Booking-ShoppingWebSite/api/TicketDetailApi' \
                          '/action/GetUserComments?productId=' + str(product_id) + '&scenicSpotId=' +\
                          str(scenic_id) + '&page=' + str(i)
            yield scrapy.Request(url=commnet_url,callback=self.scenic_comments,meta={'scenic_name':scenic_name,'scenic_id':scenic_id})

        
        # 门票名称列表
        scenic_tickets_list = response.xpath('//td[@class="ticket-title-wrapper"]/a[@class="ticket-title"]/text()').extract()
        # print(scenic_tickets_list)
        # 门票市场价价格列表
        scenic_market_list =response.xpath('//td[@class="del-price"]/strong/text()').extract()
        # print(scenic_market_list)
        # 门票携程价格列表
        scenic_ctrip_list =response.xpath('//span[@class="ctrip-price"]/strong/text()').extract()
        # print(scenic_ctrip_list)
        # 门票id列表
        scenic_detail_list = response.xpath('//tr[starts-with(@class,"ticket-info")]/@data-id').extract()
        # print(scenic_detail_list)
        # 储存门票类型列表
        scenic_type_list = [1]
        for i in range(len(scenic_tickets_list)):
            # 门票产品信息抓取
            scenic_ticket = XiechengTicket()
            # 自建id
            scenic_ticket['ticket_id'] = scenic_detail_list[i]
            # 门票名称
            scenic_ticket["ticket_name"] = scenic_tickets_list[i]
            # 门票类型
            if response.xpath('//tr[starts-with(@class,"ticket-info")]' + str([i+1]) + '/td[@class="ticket-type"]/span/text()') != []:
                scenic_ticket['scenic_type'] = response.xpath('//tr[starts-with(@class,"ticket-info")]' + str([i+1]) + '/td[@class="ticket-type"]/span/text()').extract_first()
                scenic_type_list.append(scenic_ticket['scenic_type'])
                del scenic_type_list[0]
                # print('scenic_type_list',scenic_type_list)
                # 门票提前预定时间
                scenic_ticket['scenic_reserve_time'] = response.xpath('//tr[starts-with(@class,"ticket-info")]' + str([i+1]) + '/td[3]/text()').extract_first().strip()
            else:
                scenic_ticket['scenic_type'] = scenic_type_list[0]
                # 门票提前预定时间
                scenic_ticket['scenic_reserve_time'] = response.xpath(
                    '//tr[starts-with(@class,"ticket-info")]' + str([i + 1]) + '/td[2]/text()').extract_first().strip()
            # 门票市场价格
            scenic_ticket["market_price"] = scenic_market_list[i].strip()
            # 门票携程价格
            scenic_ticket['ctrip_price'] = scenic_ctrip_list[i].strip()
            # print(detail_url)
            #  门票政策
            scenic_promise = response.xpath('//div[@class="jmp pop-content"]/text()').extract_first().strip()
            scenic_ticket['scenic_promise'] = scenic_promise
            # 景点名称
            scenic_ticket['scenic_name'] = scenic_name
            scenic_ticket['scenic_id'] = scenic_id
            # 支付方式
            scenic_ticket['ticket_payment'] = url
            # 门票详情抓取
            detail_url = 'http://piao.ctrip.com/Thingstodo-Booking-ShoppingWebSite/api/TicketStatute?resourceID=' + scenic_detail_list[i]
            yield scrapy.Request(url=detail_url,callback=self.ticket_detail,meta={"scenic_ticket":scenic_ticket})            
    def ticket_detail(self,response):
        scenic_ticket = response.meta['scenic_ticket']
        detail_html = response.text
        scenic_obj = json.loads(detail_html)
        # 门票详情
        scenic_detail = jsonpath.jsonpath(scenic_obj,'$..data')[0]
        scenic_ticket['ticket_detail'] = scenic_detail
        print('开始写入门票')
        yield scenic_ticket
        #  景点评论抓取
        # 景点评论url列表

    def scenic_comments(self,response):     
        scenic_name = response.meta['scenic_name']
        scenic_id = response.meta['scenic_id']
        comments_text = response.text
        obj_comments = json.loads(comments_text)
        if obj_comments['Comment'] != [] :
            comments = obj_comments['Comment']
            for comment in comments:
                scenic_comments = XiechengComments()
                # scenic_comments['_id'] = comment['CommentID']     #CommentID能清楚是什么
                scenic_comments['con'] = comment['con']
                scenic_comments['date'] = comment['date']
                # scenic_comments['title'] = comment['title']
                scenic_comments['grade'] = comment['grade']
                scenic_comments['uid'] = comment['uid']
                scenic_comments['Reply'] = comment['Reply']
                scenic_comments['scenic_name'] = scenic_name
                scenic_comments['scenic_id'] = scenic_id
                print('开始写入评论')
                yield scenic_comments