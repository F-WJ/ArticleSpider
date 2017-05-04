# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
# 添加域名模块(python3)
from urllib import parse

from ArticleSpider.items import JobBoleArticleItem
# md5
from ArticleSpider .utils.common import get_md5
# 添加域名模块(python2)
# import urlparse


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    # 获取一个文章内容
    # start_urls = ['http://blog.jobbole.com/110287/']
    # 获取所有所有文章内容
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # xpath用法
        # re_selector = response.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/h1')
        # re2_selector = response.xpath('''//*[@id="post-110287"]/div[1]/h1/text()''')
        # re3_selector = response.xpath('''//div[@class="entry-header"]/h1/text()''')

        """
        1.获取文章列表页中当文章url并交给scrapy下载后并进行解析
        2.获取下一页当url并交给scrapy进行下载，下载完成后交给parse
        """

        # 获取文章列表页中当文章url并交给scrapy下载后并进行解析
        # post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 有完整域名的
            # yield Request(post_url, callback=self.parse_detail)
            # 没有域名显示的(大多数网站都没有域名)
            # meta用法
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页当url并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        # 提取文章的具体字段
        front_image_url = response.meta.get("front_image_url", "")  # 提取文章封面图
        # extract_first()好处就是当万一数组为空时，防止报错，取代[0],不用再设置异常
        title = response.xpath('''//div[@class="entry-header"]/h1/text()''').extract_first("")
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·",
                                                                                                                    '').strip()
        praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract_first("")
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tag = ",".join(tag_list)

        # 传值到items.py
        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tag
        article_item["content"] = content

        # 将article_item传递到pipelines.py
        yield article_item


        # 通过css选择器提取字段
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # match_re = re.match(r".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        # comment_nums = response.css("a[href='#article-comment']::text").extract()[0]
        # match_re = re.match(r".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        #
        # content = response.css("div.entry").extract()[0]
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tag = ",".join(tag_list)
        # pass
