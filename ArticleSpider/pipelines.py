# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# pipelines作用就是拦截items数据,之后可以保存到数据库里

import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
# 将mysqldb操作变成异步化操作
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存到json文件里面（第一种方法）
# 自定义json文件导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("article.json", 'w', encoding="utf-8")

    def process_item(self, item, spider):
        # ensure_ascil防止中文乱码
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        # 返回item,是为了下一个ipipepline要处理item
        return item

    def spider_closed(self, spider):
        self.file.close()


# 保存到json文件里面（第二种方法）
class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 自定义一个pipelines,将数据保存到数据库（第一种方法,同步）
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'qaz123456789', 'article_spider', charset="utf8",
                                    use_unicode=True)
        # 用cursor操作数据库
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        # 同步操作,随着解析速度越来越快,数据里的数据越来越大,就会数据插入的速度更不上爬虫爬取的速度
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()

# 第二种插入mysql方法
# scrapy自带入库工具（异步操作）,通过from_settings.
# 在debug的时候,attributes里面能找到settings传递过来的值
# 注意dict参数名称一定要和MySQLdb.connect一样
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
       dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
       )
       dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

       return cls(dbpool)

    def  process_item(self, item, spider):
        # 使用Ttwisted插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        #  处理异步插入的异常
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_nums)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))


# 图片存放本地路径
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path

        return item
