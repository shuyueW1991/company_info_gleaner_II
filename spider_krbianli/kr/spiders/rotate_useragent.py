
# -*-coding:utf-8-*-
__author__ = "KaiTian"

"""避免被ban策略之一：使用useragent池。
使用注意：需在settings.py中进行相应的设置。
"""
import base64
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from w3lib.http import basic_auth_header

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [\
    	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5"
       ]

class ProxyMiddleware(object):
    #proxy_list = [
    #        {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    #        {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    #        {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    #        {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    #        {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    #        {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
    #        {'ip_port': '119.163.121.122:8080','user_pass':''}
    #]
    #proxy_list = [{'ip_port':'http://proxy.abuyun.com:9010','user_pass':'HR63H55U347W37PP:54913ECFA8C4CD65'}] 
    def process_request(self, request, spider):
        http_user = 'H31539Y7ZHE5X8ZD'
        http_pass = '1DACB84FC4114009'
        auth = basic_auth_header(http_user, http_pass)
        request.proxy='http://proxy.abuyun.com:9020'
        request.headers['Authorization'] = auth

        #proxyServer = "http://proxy.abuyun.com:9010"
        #proxyUser = "H4C9Q476M1927EJP"
        #proxyPass = "10DBB2F826A212CA"
        #proxyAuth = base64.encodestring((proxyUser + ":" + proxyPass).encode()).decode().replace('\n', '')
        #proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        #request.meta["proxy"] = proxyServer
        #request.headers["Proxy-Authorization"] = proxyAuth
        #proxy = random.choice(self.proxy_list)
        #if proxy['user_pass'] is not None:
        #    request.meta['proxy'] = "http://%s" % proxy['ip_port']
        #    encoded_user_pass = base64.encodestring(proxy['user_pass'].encode()).decode().replace('\n', '')
        #    request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        #    print("**************ProxyMiddleware have pass************" + proxy['ip_port'])
        #else:
        #    print("**************ProxyMiddleware no pass************" + proxy['ip_port'])
        #    request.meta['proxy'] = "http://%s" % proxy['ip_port']
