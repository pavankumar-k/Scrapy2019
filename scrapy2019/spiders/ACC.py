# -*- coding: utf-8 -*-
import scrapy

class AccSpider(scrapy.Spider):
    name = 'ACC'
    part = "https://www.sciencedirect.com"

    def start_requests(self):
        # url = 'https://www.sciencedirect.com/journal/journal-of-the-american-college-of-cardiology/vol/71/issue/11/suppl/S?page='
        url = 'https://www.sciencedirect.com/journal/journal-of-the-american-college-of-cardiology/vol/69/issue/11/suppl/S?page='
        for i in range(1,27):
            yield scrapy.Request(url+str(i),callback=self.parse)


    def parse(self, response):
        urls = response.css("h3.text-m.u-font-serif.u-display-inline a::attr(href)").extract()
        for url in urls:
            with open("links17.txt",'a+') as file:
                file.write(self.part+str(url)+'\n')



