# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    # items只有Field类型
    title = scrapy.Field()  # 文章标题
    create_date = scrapy.Field()  # 创建文章时间
    url = scrapy.Field()  # 文章地址
    url_object_id = scrapy.Field()  # 将url变成固定长度（将url变成md5）
    front_image_url = scrapy.Field()  # 封面图
    front_image_path = scrapy.Field()  # 图片本地存放地址
    praise_nums = scrapy.Field()  # 点赞数
    comment_nums = scrapy.Field()  # 评论数
    fav_nums = scrapy.Field()  # 收藏数
    tags = scrapy.Field()  # 文章标签
    content = scrapy.Field()  # 文章内容




