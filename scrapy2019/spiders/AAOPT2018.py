# -*- coding: utf-8 -*-
import scrapy


class AaoptSpider(scrapy.Spider):
    name = 'AAOPT2018'
    start_urls = ['https://www.aaopt.org/knowledge-base-search?sortBy=tdt_cms_CustomPublishDate&Year=2018']

    def parse(self, response):
        urls = response.css("div.result-titles > a::attr(href)").extract()
        for url in urls:
            yield response.follow(url,callback= self.abst)


        pagenxt = response.css("a.pagerNext::attr(href)").extract()
        if len(pagenxt)>0:
            yield response.follow(pagenxt[0], callback=self.parse)


    def abst(self, response):
        lis = response.css("div.content-box > p")
        det = ''
        for a in lis:
            det += "".join(a.css(" ::text").extract())+'|#|'

        yield{
            'url': response.url,
            'title': response.css("h1.page-title ::text").extract_first().strip(),
            'author': response.css("h2.page-subtitle ::text").extract_first().strip(),
            'text': "\n".join([x.strip() for x in response.css("div#PageContentPlaceholder_T3E8653F3001_Col02 ::text").extract()]).strip(),
            'details': det
        }
