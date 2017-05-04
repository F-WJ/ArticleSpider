# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# pipelines作用就是拦截items数据,之后可以保存到数据库里

import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存到json文件里面（第一种方法）
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
#
#
#
class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()


# 图片存放本地路径
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path

        return item
