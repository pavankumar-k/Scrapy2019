# -*- coding: utf-8 -*-
import scrapy
import logging

class AstroSpider(scrapy.Spider):
    name = 'ASTRO2'
    url = 'https://www.redjournal.org'
    #
    start_urls = ['https://www.redjournal.org/issue/S0360-3016(16)X0010-7']

    def parse(self, response):
        lis = response.css('h2.title > a::attr(href)').extract()
        logging.info('urlsLENGTH:'+str(len(lis)))
        for l in lis:
            yield response.follow(self.url+l,callback = self.product)
        t = response.css('li.next > a::attr(href)').extract_first()
        if t is not None:
            yield response.follow(self.url+t,callback = self.parse)

    def product(self,response):
        title = response.css("h1.articleTitle::text").extract_first()
        doi= ''.join(response.css("div.doi ::text").extract())
        text = ''.join(response.css("div.body > div.content ::text").extract())
        disc = ''.join(response.css("div.footnotes ::text").extract())
        alis = response.css('div.author')
        affli = ''.join(response.css('div.affiliation ::text').extract())
        for a in alis:
            auth = a.css('a.openAuthorLayer.layerTrigger ::text').extract_first()
            aff = ';'.join(a.css('ul.affiliations ::text').extract())
            if len(aff)==0:
                aff = affli
            if aff is None:
                aff = ''
            yield{
                   'url':response.url,
                   'author':auth,
                   'affli':aff,
                   'title':title,
                   'doi':doi,
                   'text':text,
                   'disc':disc}
	    
