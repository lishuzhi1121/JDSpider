# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class goodsItem(item):
	"""docstring for goodsItem"""
	link = scrapy.Field()				# 商品链接
	ID = scrapy.Field()					# 商品ID
	name = scrapy.Field()				# 商品名称
	comment_num = scrapy.Field()		# 评论数
	shop_name = scrapy.Field()			# 店家名称
	price = scrapy.Field()				# 商品价格
	commentVersion = scrapy.Field()		# 为了得到评论地址需要该字段
	score1count = scrapy.Field()		# 1星评论数
	score2count = scrapy.Field()		# 2星评论数
	score3count = scrapy.Field()		# 3星评论数
	score4count = scrapy.Field()		# 4星评论数
	score5count = scrapy.Field()		# 5星评论数

class commentItem(Item):
	"""docstring for commentItem"""
	user_name = scrapy.Field()			# 该评论的用户名
	user_ID = scrapy.Field()			# 该评论用户的ID
	userProvince = scrapy.Field()		# 该评论用户的地区
	content = scrapy.Field()			# 评论内容
	good_ID = scrapy.Field()			# 评论商品的ID
	good_name = scrapy.Field()			# 评论商品的名称
	date = scrapy.Field()				# 评论时间
	replyCount = scrapy.Field()			# 该评论的回复数
	score = scrapy.Field()				# 评分
	status = scrapy.Field()				# 状态
	title = scrapy.Field()
	userLevelId = scrapy.Field()
	userRegisterTime = scrapy.Field()	# 用户注册时间
	productColor = scrapy.Field()		# 商品颜色
	productSize = scrapy.Field()		# 商品大小
	userLevelName = scrapy.Field()		# 用户等级名称:银牌会员,金牌会员等
	UserClientShow = scrapy.Field()		# 来自什么平台,如京东客户端
	isMobile = scrapy.Field()			# 是否来自手机
	days = scrapy.Field()				# 天数
	commentTags = scrapy.Field()		# 标签

