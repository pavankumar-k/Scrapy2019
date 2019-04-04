# -*- coding: utf-8 -*-
import scrapy
import logging

class EsmowcgcSpider(scrapy.Spider):
    name = 'ESMOWCGC'
    url = 'https://oncologypro.esmo.org/'
    start_urls = ['https://oncologypro.esmo.org/Meeting-Resources/ESMO-World-Congress-on-Gastrointestinal-Cancer-2017?SearchText=&dateFilter=&presenter_filter=&session_filter=&hasabstract_filter=on&sort=published_asc']
    i = 0
    j=1

    def parse(self, response):
        urls = response.css("div.attribute-title > h2 > a::attr(href)").extract()
        self.i+=len(urls)
        for a in urls:
           yield response.follow(self.url+a,callback=self.product,dont_filter=True)
        logging.info("PAGE NUM:"+str(self.j))
        logging.info("LENGTH OF URLS:"+str(self.i)) 
        page = response.css('a[title="Next"]::attr(href)').extract_first()
        if page is not None:
            self.j+=1
            yield response.follow(self.url+page,callback=self.parse,dont_filter=True)
            
    def product(self,response):
        li = response.css('table.mobile tr')
        if len(li)<7 or len(li)>7:
            raise "Error element Not found"
        yield{
                'url':response.url,
                'title':response.css("h1 ::text").extract_first(),
                'text':'\n'.join([x.strip() for x in response.css('div.row.no-margin ::text').extract()]),
                'date':' '.join([x.strip() for x in li[0].css('::text').extract()]),
                'event':' '.join([x.strip() for x in li[1].css('::text').extract()]),
                'session':' '.join([x.strip() for x in li[2].css('::text').extract()]),
                'topics':';'.join([x.strip() for x in li[3].css('::text').extract()]),
                'citation':' '.join([x.strip() for x in li[5].css('::text').extract()]),
                'author':''.join([x.strip() for x in li[6].css('::text').extract()])
                }
    
