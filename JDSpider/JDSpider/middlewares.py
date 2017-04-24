# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

__author__ = 'Sands_Lee'
from scrapy import signals
from settings import PROXIES
import random
import base64

# 主要用于动态获取User-Agent,User-Agent列表USER_AGENTS在settings.py中进行配置
class RandomUserAgent(object):
    """Randomly rotate user agents based on alist of predefined ones"""
    def __init__(self, agents):
        # super(RandomUserAgent, self).__init__()
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    @classmethod
    def process_request(self, request, spider):
        print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

# 用于切换代理,proxy列表PROXIES也是在settings.py中进行配置
class ProxyMiddleware(object):
    """Change Proxy"""
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = 'http://%s' % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
        

