# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class AhaSpider(scrapy.Spider):
    name = 'Aha'
    # allowed_domains = ['aga']
    start_urls = ['https://www.ahajournals.org/toc/circ/138/Suppl_1',
                  'https://www.ahajournals.org/toc/circ/136/suppl_1']

    def parse(self, response):
        surls = response.css("ul.expandable-list__body > li > a::attr(href)").extract()
        for surl in surls:
            yield response.follow("https://www.ahajournals.org"+surl, callback= self.parseurl)

    def parseurl(self, response):
        urls = response.css("h3.meta__title.meta__title__margin > a::attr(href)").extract()
        for url in urls:
            yield response.follow("https://www.ahajournals.org"+url, callback= self.parseprod)

    def parseprod(self,response):

        aut = response.css("div.author-info.accordion-tabbed__content")
        for a in aut:
            alis = [x.strip() for x in a.css("::text").extract() if len(x.strip())>0]
            yield{
                "url":response.url,
                "subtitle":response.css("h5.supplement-heading__subject-title ::text").extract_first(),
                "session":response.css("h5.supplement-heading__subject-group-title ::text").extract_first(),
                "title":response.css("h1.citation__title ::text").extract_first(),
                "author": alis[0],
                "affli": "; ".join(alis[1:-1]),
                "date": "\n".join(response.css("div.epub-section ::text").extract()),
                "text":"\n".join(response.css("div.hlFld-Abstract ::text").extract()),
                "disc":"\n".join(response.css("div.NLM_author-notes ::text").extract())
            }

