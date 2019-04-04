# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import logging

class Ae2018Spider(scrapy.Spider):
    name = 'AE2018'
    url = 'https://www.alzheimer-europe.org'
    logger = logging.getLogger()
    
    def start_requests(self):
        starturl = 'https://www.alzheimer-europe.org/Conferences/Previous-conferences/2018-Barcelona/Detailed-programme-abstracts-and-presentations'
        self.logger.info('STARTED SCRAPING')
        yield SplashRequest(starturl,self.parse,args={'html':1,'wait':5.0})

    def parse(self, response):
        li = response.css('div.grid_8>div.article>h4>a::attr(href)').extract()
        li.extend([self.url+x.strip() for x in response.css('div.wrap>ol>li>a::attr(href)').extract()])
        self.logger.info('TOTAL NO OF URLS:'+str(len(li)))
        for a in li:
            yield SplashRequest(a,self.parseUrl,args={'html': 1,'wait':5.0})
    
    def parseUrl(self,response):
        self.logger.warning('STARTING URL:'+str(response.url))
        ses = '\n'.join(response.css('div.grid_8>h1.fh2 ::text').extract())
        arlis = response.css('div.article>*')
        i=0
        while i<len(arlis):
            tagname = arlis[i].xpath('name()').extract_first()
            if tagname == 'h4':
                tit = '\n'.join(arlis[i].css(' ::text').extract())
                i+=1
                if (i+1)>=len(arlis):
                    break
                auth = '\n'.join(arlis[i].css(' ::text').extract())
                i+=1
                affli = '\n'.join(arlis[i].css(' ::text').extract())
                i+=1
                data = ''
                while i<len(arlis):
                    tagname = arlis[i].xpath('name()').extract_first()
                    if tagname == 'h4':
                        break
                    temp = arlis[i].css(' ::text').extract()
                    if temp is not None:
                        data +='\n'.join(temp)  
                    i+=1
                yield{
                        'url': response.url,
                        'title': tit,
                        'session': ses,
                        'auth':auth,
                        'affli':affli,
                        'data':data
                        }
            else:
                i+=1
            
            
