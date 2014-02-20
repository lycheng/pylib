#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

__author__ = 'lycheng'
__email__ = "lycheng997@gmail.com"
__date__ = '2014-02-20'

from threadpool import ThreadPool

from BeautifulSoup import BeautifulSoup
from requests import get

from time import sleep
import os

class ComicDownload(ThreadPool):
    index = 'http://*.*.com/17/'
    path = '/home/lycheng/comic/fa'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':None #注意如果依然不能抓取，这里可以设置抓取网站的host
             }
    log_addr = path + "/" + "log"
    logs = set()

    def download_img(self, src, file_path):
        print "%s -> %s" % (src, file_path)
        img = get(src, headers=self.headers).content
        fp = open(file_path, "w")
        fp.write(img)
        fp.close()

    def get_chapter_urls(self):
        page = get(self.index).content
        soup = BeautifulSoup(page)
        container = soup.find(attrs = {'id': 'content'}).findAllNext('li')
        urls = []
        for li in container:
            a = BeautifulSoup(str(li)).find('a')
            try:
                if str(a['href'])[:-1] not in self.logs:
                    urls.append(str( a['href'])[:-1])
            except:
                continue

        return urls

    def read_log(self):
        """ 读取 log 获取已经下载的章节
        """
        try:
            fp = open(self.log_addr, "r")
        except:
            fp = None
        if fp:
            lines = fp.readlines()
            for log in lines:
                self.logs.add(log[:-1])
            fp.close()

    def run(self):
        """ 读取目录内容并加入到队列中去
        """
        self.read_log()
        urls = self.get_chapter_urls()
        for url in urls:
            self.queue.put(url)
        while self.queue.qsize():
            fp = open(self.log_addr, 'w')
            for log in self.logs:
                fp.write(str(log))
                fp.write('\n')
            sleep(60)
        sleep(360)

    def serve(self, chapter):
        """ 下载每个章节的所有图片
        """
        address = self.index + chapter
        dir_path = self.path + '/' + chapter + "/"
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        last = ''
        suffix = "index_%d.html"
        for i in xrange(0, 200):
            page = address + '/' + suffix % i
            page_content = get(page).content
            soup = BeautifulSoup(page_content)
            img_src = soup.find('img', id="mhpic")["src"]
            if last == img_src:
                break
            last = img_src
            extend = img_src[img_src.rindex(".") :]
            self.download_img(img_src, dir_path+str(i)+extend)
        self.logs.add(chapter)

if __name__ == "__main__":
    obj = ComicDownload()
    obj.start()
