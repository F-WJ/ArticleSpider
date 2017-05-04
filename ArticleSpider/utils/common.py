# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = '17-5-2 下午8:02'
import hashlib


# 将url变成md5
def get_md5(url):
    # 在python中,str就是unicode
    if isinstance(url, str):
        url = url.encode()
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# python3要转utf8编码,python2不用
if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("utf-8")))
