# -*- coding: utf-8 -*-
# author: ailin
# simple web spider
import urllib
import urllib2
import sys
import re
import gzip
from socket import error as SocketError
import errno


class Spider(object):
    """docstring for Spider"""
    visited_urls = []
    query = []
    url_map = {}  #store as current_url: last_url 
    start_url = ""
    end_url = ""
    count = 0
    pattern = re.compile('<a.*?href="(\w+)://(.*?)".*?>')
    def __init__(self, start_url, end_url):
        super(Spider, self).__init__()
        self.start_url = start_url
        self.end_url = end_url
        self.query.append(self.start_url)
        self.url_map[self.start_url] = ""

    """search"""
    def run(self):
        pass


    """get urls from given url"""
    """ return string[] urls"""
    def get_urls(self, url):
        result = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
            }
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=5)
        except urllib2.URLError, e:
            print e.reason
            return []
        except SocketError, e:
            print "socket error"
            return []
        except:
            print "I dont know.But there must be something wrong_(:з」∠)_"
            return []
        else:
            try:
                web_page = response.read()
            except:
                print "timeout raised and caught"
                return []
            else:
                content = self.get_unicode_content(web_page, response.info().get('Content-Type'))
                
                for item in re.findall(self.pattern, content):
                    new_url = item[0]+"://"+item[1][:item[1].find("/")]
                    result.append(new_url)
                return result

    """get unicode webpage content"""
    """return unicode urls"""
    def get_unicode_content(self, webpage, contentType="utf-8"):
        print contentType
        if not contentType:
            contentType = 'utf-8'

        if contentType.find('gbk'):
            return webpage.decode('gbk', 'ignore')
        elif contentType.find('utf-8'):
            return webpage.decode('utf-8')
        elif contentType.find('gb2312'):
            return webpage.decode('gb2312')
        else:
            return webpage
        

    """trace routes"""
    def trace(self, url):
        result = []
        count = 0;
        print self.url_map[self.start_url]
        while url:
            result.append(url)
            url = self.url_map[url.encode('utf-8')]
        while result:
            count = count+1
            print result.pop()
        print "Reached: " + str(self.count), "Link length: " + str(count)


class BfsSpider(Spider):
    def __init__(self, start_url, end_url):
        Spider.__init__(self, start_url, end_url)

    """bfs search"""
    def run(self):
        while self.query:
            if self.query:
                cur = self.query[0]
                self.visited_urls.append(cur)
                del self.query[0]
                for new_url in self.get_urls(cur):
                    if  new_url not in self.query and new_url  not in self.visited_urls:
                        self.count = self.count+1
                        self.url_map[new_url] = cur
                        if new_url == self.end_url:
                            print "success!"
                            self.trace(new_url)
                            return
                        else:
                            print new_url
                            self.query.append(new_url)

class BiSpider(Spider):
    """Bidirection Search"""
    back_query = []
    back_visited_urls = []
    back_url_map = {}
    def __init__(self, start_url, end_url):
        Spider.__init__(self, start_url, end_url)
        self.back_query.append(end_url)
        self.back_url_map[end_url] = "" # forword end_url->nothing

    def run(self):
        # normal forward query
        while self.query or self.back_query:
            if self.query:
                cur = self.query[0]
                print cur
                self.visited_urls.append(cur)
                del self.query[0]
                for new_url in self.get_urls(cur):
                    if  new_url not in self.query and new_url not in self.visited_urls:
                        self.count = self.count+1
                        self.url_map[new_url] = cur # backword cur->last
                        if new_url in self.back_visited_urls:
                            print "success!"
                            self.trace(new_url)
                            return
                        else:
                            print new_url
                            self.query.append(new_url)
            if self.back_query:
                cur = self.back_query[0]
                self.back_visited_urls.append(cur)
                del self.back_query[0]
                for new_url in self.get_urls(cur):
                    if new_url not in self.back_query and new_url not in self.back_visited_urls:
                        self.count = self.count + 1
                        self.back_url_map[new_url] = cur  #forword cur->next
                        if new_url in self.visited_urls:
                            print "success!"
                            self.trace(new_url)
                            return
                        else:
                            print new_url
                            self.back_query.append(new_url) 

    def trace(self, url):
        temp1 = []
        temp2 = []
        hold = url
        while url:
            temp1.append(url)
            url = self.url_map[url]
        url = hold
        while url:
            url = self.back_url_map[url]
            if url:
                temp2.append(url)
        result = temp1[::-1] + temp2
        for url in result:
            print url
        print "Reached: " + str(self.count), "Link length: " + str(len(result))



if __name__ == "__main__":
    if len(sys.argv) >= 2:
        cuteSpider = BiSpider(sys.argv[1], sys.argv[2])
        cuteSpider.run()
    else:
        print "Sorry.You should input the start url and the end url"
        print "eg: python spider.py http://www.baidu.com http://www.zhihu.com"

