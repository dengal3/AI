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

class Url(object):
    """docstring for Url"""
    cur_url = ""
    last_url = ""
    def __init__(self, cur_url, last_url):
        super(Url, self).__init__()
        self.cur_url = cur_url
        self.last_url = last_url

    def get_cur_url():
        return self.cur_url
        
    def get_last_url():
        return self.last_url


class Spider(object):
    """docstring for Spider"""
    visited_urls = []
    query = []
    url_map = {}  #store as current_url: last_url 
    start_url = ""
    end_url = ""
    pattern = re.compile('<a.*?href="(\w+)://(.*?)".*?>')
    def __init__(self, start_url, end_url):
        super(Spider, self).__init__()
        self.start_url = start_url
        self.end_url = end_url
        self.query.append(self.start_url)
        self.url_map[self.start_url] = ""

    """bfs search"""
    def run(self):
        while self.query:
            cur = self.query[0]
            self.visited_urls.append(cur)
            del self.query[0]
            for new_url in self.get_urls(cur):
                if  new_url not in self.query and new_url  not in self.visited_urls:
                    self.url_map[new_url] = cur
                    if new_url == self.end_url:
                        print "success!"
                        self.trace(new_url)
                        return
                    else:
                        print new_url
                        self.query.append(new_url)

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
        result.append(url)
        print self.url_map[self.start_url]
        while url:
            url = self.url_map[url.encode('utf-8')]
            result.append(url)
        while result:
            print result.pop()



    

if __name__ == "__main__":
    if sys.argv[1] and sys.argv[2]:
        cuteSpider = Spider(sys.argv[1], sys.argv[2])
        cuteSpider.run()
    else:
        print "Sorry.You should input the start url and the end url"
        print "eg: python spider.py http://www.baidu.com http://www.zhihu.com"




# start_url = sys.argv[1]
# end_url = sys.argv[2]
# visited = []
# pattern = re.compile('<a.*?href="(\w+)://(.*?)".*?>')

# request = urllib2.Request(start_url)
# response = urllib2.urlopen(request)
# web_page = response.read()
# if response.info().get('Content-Encoding') is "gzip":
#     buf = StringIO.StringIO(response.read())
#     f = gzip.GzipFile(fileobj=buf)
#     content = f.read().decode("utf-8")
# else:
#     content = web_page.decode('utf-8')
# for item in re.findall(pattern, content):
#     print item[1][:item[1].find("/")]