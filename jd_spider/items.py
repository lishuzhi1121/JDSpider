# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class goodsItem(Item):
    product_id = Field()         # 商品ID
    product_name = Field()       # 商品名字
    shop_name = Field()          # 店家名字
    product_price = Field()      # 价钱
    product_link = Field()       # 商品链接
    comment_count = Field()      # 评论人数
    comment_version = Field()    # 为了得到评论的地址需要该字段
    score1count = Field()        # 评分为1星的人数
    score2count = Field()        # 评分为2星的人数
    score3count = Field()        # 评分为3星的人数
    score4count = Field()        # 评分为4星的人数
    score5count = Field()        # 评分为5星的人数


class commentItem(Item):
    user_id = Field()            # 评论用户的ID
    user_name = Field()          # 评论用户的名字
    user_province = Field()      # 评论用户来自的地区
    user_level_id = Field()      # 用户等级
    user_level_name = Field()    # 银牌会员，钻石会员等
    product_id = Field()         # 评论的商品ID
    product_name = Field()       # 评论的商品名字
    comment_content = Field()    # 评论内容
    comment_date = Field()       # 评论时间
    reply_count = Field()        # 回复数
    score = Field()              # 评分
    status = Field()             # 状态
    title = Field()
    product_color = Field()      # 商品颜色
    product_size = Field()       # 商品大小
    user_client_show = Field()   # 来自什么 比如来自京东客户端
    is_mobile = Field()          # 是否来自手机
    comment_days = Field()       # 天数
    comment_tags = Field()       # 标签
