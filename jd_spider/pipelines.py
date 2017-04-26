# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log
import chardet

SETTINGS = get_project_settings()


class MySQLPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS['DB_HOST'],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor
                                            )
        self.stats = stats
        self.dbpool.runInteraction(self._create_table)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _create_table(self, tx):
        drop_sql = "DROP TABLE IF EXISTS jd_products"
        tx.execute(drop_sql)

        creat_sql = "CREATE TABLE jd_products (product_id BIGINT DEFAULT NULL, product_name VARCHAR(128) DEFAULT NULL, shop_name VARCHAR(128) DEFAULT NULL, product_price DOUBLE DEFAULT NULL, product_link VARCHAR(128) DEFAULT NULL, comment_count INT DEFAULT NULL, comment_version INT DEFAULT NULL, score1count INT DEFAULT 0, score2count INT DEFAULT 0, score3count INT DEFAULT 0, score4count INT DEFAULT 0, score5count INT DEFAULT 0)"
        tx.execute(creat_sql)
        print "Create table jd_products success."

    def _insert_record(self, tx, item):
        product_id = item['product_id'][0]
        product_name = item['product_name'][0]
        shop_name = item['shop_name'][0]
        product_price = str(item['product_price'])
        product_link = item['product_link'][0]
        comment_count = str(item['comment_count'])

        comment_version = str(item['comment_version'])
        comment_version = comment_version[1:-1]

        score1count = str(item['score1count'])
        score2count = str(item['score2count'])
        score3count = str(item['score3count'])
        score4count = str(item['score4count'])
        score5count = str(item['score5count'])

        product_id = product_id.encode('utf-8')
        product_name = product_name.encode('utf-8')
        shop_name = shop_name.encode('utf-8')
        product_price = product_price.encode('utf-8')
        product_link = product_link.encode('utf-8')
        comment_count = comment_count.encode('utf-8')
        comment_version = comment_version.encode('utf-8')
        score1count = score1count.encode('utf-8')
        score2count = score2count.encode('utf-8')
        score3count = score3count.encode('utf-8')
        score4count = score4count.encode('utf-8')
        score5count = score5count.encode('utf-8')

        insert_sql = "INSERT INTO jd_products VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (product_id, product_name, shop_name, product_price, product_link, comment_count, comment_version, score1count, score2count, score3count,
               score4count, score5count)

        tx.execute(insert_sql)
        print "OK -> " + str(product_id)

    def _handle_error(self, e):
        log.err(e)


class CommentPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS['DB_HOST'],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor
                                            )
        self.stats = stats
        self.dbpool.runInteraction(self._create_table)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _create_table(self, tx):
        drop_sql = "DROP TABLE IF EXISTS jd_comments"
        tx.execute(drop_sql)

        creat_sql = "CREATE TABLE jd_comments (user_id BIGINT DEFAULT NULL, user_name VARCHAR(128) DEFAULT NULL, user_province VARCHAR(128) DEFAULT NULL, user_level_id INT DEFAULT NULL, user_level_name VARCHAR(128) DEFAULT NULL, product_id BIGINT DEFAULT NULL, product_name VARCHAR(128) DEFAULT NULL, comment_content VARCHAR(255) DEFAULT NULL, comment_date DATETIME DEFAULT NULL, reply_count INT DEFAULT 0, score INT DEFAULT 0, status TINYINT DEFAULT NULL, title VARCHAR(128) DEFAULT NULL, product_color VARCHAR(128) DEFAULT NULL, product_size VARCHAR(128) DEFAULT NULL, user_client_show VARCHAR(128) DEFAULT NULL, is_mobile VARCHAR(8) DEFAULT NULL, comment_days INT DEFAULT NULL, comment_tags VARCHAR(255) DEFAULT NULL)"
        tx.execute(creat_sql)
        print "Create table jd_comments success."

    def _insert_record(self, tx, item):
        user_id = item['user_id']
        user_name = item['user_name']
        user_province = item['user_province']
        user_level_id = item['user_level_id']
        user_level_name = item['user_level_name']
        product_id = item['product_id']
        product_name = item['product_name']
        comment_content = item['comment_content']
        comment_date = item['comment_date']
        reply_count = item['reply_count']
        score = item['score']
        status = item['status']
        title = item['title']
        product_color = item['product_color']
        product_size = item['product_size']
        user_client_show = item['user_client_show']
        is_mobile = item['is_mobile']
        comment_days = item['comment_days']
        comment_tags = item['comment_tags']

        insert_sql = "INSERT INTO jd_comments VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
              "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (user_id, user_name, user_province, user_level_id, user_level_name, product_id, product_name, comment_content,
               comment_date, reply_count, score, status, title, product_color,
               product_size, user_client_show, is_mobile, comment_days, comment_tags)

        tx.execute(insert_sql)
        print "OK -> " + str(user_id)

    def _handle_error(self, e):
        log.err(e)
