# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from jd_spider.items import goodsItem, commentItem
from scrapy.selector import Selector
import re
import json
import xlrd


class comment_spider(Spider):
    name = "comments"
    xlrd.Book.encoding = "utf-8"
    data = xlrd.open_workbook("goods.xls")
    # goods为要抓取评论的商品信息，提供一个goods.xls文件供参考,第1列：商品ID；第2列：商品评论数；第3列：商品的commentVersion
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    good_id = table.col_values(0)  # 商品ID
    comment_n = table.col_values(1)  # 商品评论数
    comment_V = table.col_values(2)  # 商品评论的commentVersion

    start_urls = []
    for i in range(len(good_id)):  # 一件商品一件商品的爬
        good_num = int(good_id[i])
        comment_total = int(comment_n[i])
        if comment_total % 10 == 0:  # 算出评论的页数，一页10条评论
            page = comment_total/10
        else:
            page = comment_total/10 + 1
        # 用page替换数字3即可爬取所有评论
        for k in range(0, 2):
            url = "http://sclub.jd.com/productpage/p-" + str(good_num) + "-s-0-t-3-p-" + str(k) \
                  + ".html?callback=fetchJSON_comment98vv" + str(comment_V[i])
            start_urls.append(url)

    def parse(self, response):
        temp1 = response.body.split('productAttr')
        str = '{"productAttr' + temp1[1][:-2]
        str = str.decode("gbk").encode("utf-8")
        js = json.loads(unicode(str, "utf-8"))
        comments = js['comments']  # 该页所有评论

        items = []
        for comment in comments:
            item1 = commentItem()
            item1['user_id'] = comment['id']
            item1['user_name'] = comment['nickname']
            item1['user_province'] = comment['userProvince']
            item1['user_level_id'] = comment['userLevelId']
            item1['user_level_name'] = comment['userLevelName']
            item1['product_id'] = comment['referenceId']
            item1['product_name'] = comment['referenceName']
            item1['comment_content'] = comment['content']
            item1['comment_date'] = comment['referenceTime']
            item1['reply_count'] = comment['replyCount']
            item1['score'] = comment['score']
            item1['status'] = comment['status']

            title = ""
            if comment.has_key('title'):
                item1['title'] = comment['title']
            item1['title'] = title
            
            item1['product_color'] = comment['productColor']
            item1['product_size'] = comment['productSize']
            item1['user_client_show'] = comment['userClientShow']
            item1['is_mobile'] = comment['isMobile']
            item1['comment_days'] = comment['days']

            tags = ""
            if comment.has_key('commentTags'):
                for i in comment['commentTags']:
                    tags = tags + i['name'] + " "
            item1['comment_tags'] = tags

            items.append(item1)
        return items

