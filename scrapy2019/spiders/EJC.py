# -*- coding: utf-8 -*-
import scrapy

class EjcSpider(scrapy.Spider):
    name = 'EJC'
    url = 'https://www.ejcancer.com'
    start_urls = ['https://www.ejcancer.com/issue/S0959-8049(18)X0005-7']

    def parse(self, response):
        urls = response.css('div.articleTitle a::attr(href)').extract()
        for a in urls:
            yield response.follow(self.url+a,callback=self.product)
        page =  response.css('li.next a::attr(href)').extract_first()
        if page is not None:
            yield response.follow(self.url+page,callback=self.parse)
        
    def product(self,response):
        li = response.css('div.authorGroup > div.author')
        abst = '\n'.join([x.strip() for x in response.css('div.abstract ::text').extract()])
        cont = '\n'.join([x.strip() for x in  response.css('div#artTabContent > div.content ::text').extract()])
        keys = ''.join([x.strip() for x in response.css('div.keywords ::text').extract()])
        for a in li:
            yield{
                "url":response.url,
                'title': ''.join([x.strip() for x in  response.css('h1.articleTitle ::text').extract()]),
                'author': a.css('a.openAuthorLayer.layerTrigger::text').extract_first(),
                'affli':';'.join([x.strip() for x in set(a.css('ul.affiliations li::text').extract())]),
                'session': ';'.join([x.strip() for x in response.css('div.miscellaneous ::text').extract()]),
                'doi': ' '.join([x.strip() for x in response.css('div.doi ::text').extract()]),
                'text': abst+'\n'+cont,
                'keywords':keys
                }