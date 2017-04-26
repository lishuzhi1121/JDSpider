# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from jd_spider.items import goodsItem
from scrapy.selector import Selector
import scrapy
import re
import json


class jd_spider(Spider):
    name = "products"
    start_urls = []
    for i in range(1, 3):   # 这里请自己设置页数，目前只能抓取平板电脑分类下前3页的商品
        url = 'http://list.jd.com/list.html?cat=670,671,2694&page=' + str(i)
        start_urls.append(url)

    def parse_price(self, response):
        item1 = response.meta['item']
        temp1 = response.body.split('jQuery([')
        s = temp1[1][:-4]  # 获取到需要的json内容
        js = json.loads(str(s))  # js是一个list
        if js.has_key('pcp'):
            item1['product_price'] = js['pcp']
        else:
            item1['product_price'] = js['p']
        return item1

    def parse_getCommentnum(self, response):
        item1 = response.meta['item']
        # response.body是一个json格式的
        js = json.loads(str(response.body))
        item1['score1count'] = js['CommentsCount'][0]['Score1Count']
        item1['score2count'] = js['CommentsCount'][0]['Score2Count']
        item1['score3count'] = js['CommentsCount'][0]['Score3Count']
        item1['score4count'] = js['CommentsCount'][0]['Score4Count']
        item1['score5count'] = js['CommentsCount'][0]['Score5Count']
        item1['comment_count'] = js['CommentsCount'][0]['CommentCount']
        num = item1['product_id']  # 获得商品ID
        s1 = str(num)
        url = "http://pm.3.cn/prices/pcpmgets?callback=jQuery&skuids=" + s1[3:-2] + "&origin=2"
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_price)

    def parse_detail(self, response):
        item1 = response.meta['item']
        sel = Selector(response)

        temp = response.body.split('commentVersion:')
        pattern = re.compile("[\'](\d+)[\']")
        if len(temp) < 2:
            item1['comment_version'] = -1
        else:
            match = pattern.match(temp[1][:10])
            item1['comment_version'] = match.group()

        url = "http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=" + str(item1['product_id'][0])
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_getCommentnum)

    def parse(self, response):  # 解析搜索页
        sel = Selector(response)  # Xpath选择器
        goods = sel.xpath('//li[@class="gl-item"]')
        for good in goods:
            item1 = goodsItem()
            item1['product_id'] = good.xpath('./div/@data-sku').extract()
            item1['product_name'] = good.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
            item1['shop_name'] = good.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract()
            item1['product_link'] = good.xpath('./div/div[@class="p-img"]/a/@href').extract()
            url = "http:" + item1['product_link'][0] + "#comments-list"
            yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_detail)

