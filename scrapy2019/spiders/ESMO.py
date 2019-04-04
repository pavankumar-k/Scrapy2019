# -*- coding: utf-8 -*-
import scrapy


class EsmoSpider(scrapy.Spider):
    name = 'ESMO18'
    
    def start_urls(self):
        yield Request(url= '', callback=self.parse)
        

    def parse(self, response):
        
        pass
