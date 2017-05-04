# -*- coding:utf-8 -*-

from scrapy.cmdline import execute

import sys
import os

# print(os.path.dirname(os.path.abspath(__file__)))
# 查找main.py主目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])
