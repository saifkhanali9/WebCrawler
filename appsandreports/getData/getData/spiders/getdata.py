# -*- coding: utf-8 -*-
import scrapy
import json

class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['example.com']
    tempArray = []
    with open(r'C:\Saif\Office\WebCrawler\Appsandreports\Files\allSoftwareUrls.json') as f:
        d = json.load(f)
        for i in d:
            # print(i['urls'])
            tempArray = tempArray + i['urls']
    urlArray = []
    for i in tempArray:
        if i not in urlArray:
            urlArray.append(i)
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
