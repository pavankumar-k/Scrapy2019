# -*- coding: utf-8 -*-
import scrapy


class Ece2016Spider(scrapy.Spider):
    name = 'ECE2016'
    url = 'https://www.endocrine-abstracts.org'
    start_urls = ['https://www.endocrine-abstracts.org/ea/0041/eposters']

    def parse(self, response):
        i = 0
        urls =  response.css('div.col-md-1.text-right > a::attr(href)').extract()
        while i<len(urls):
            if i%2==0:
                yield response.follow(self.url+urls[i].strip(),callback=self.products)
            i+=1
            
    def products(self,response):
        
        yield{
                'url':response.url,
                
                }