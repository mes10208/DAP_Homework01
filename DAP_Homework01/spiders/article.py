# -*- coding: utf-8 -*-
import scrapy
from DAP_Homework01.items import articles, article

class ArticleSpider(scrapy.Spider):
	name = 'article'
	allowed_domains = ['www.w3schools.com']
	start_urls = ['https://www.w3schools.com/html/']

	def parse(self, response):
		host = self.allowed_domains[0]

		for link in response.css("#leftmenuinnerinner > a"):
			title = f"{link.css('a::text').get()}"
			link = self.start_urls[0] + f"{link.attrib.get('href')}"
			yield response.follow(link, callback=self.parse_detail, meta={'link':link, 'title':title})

	def parse_detail(self, response):
		items = articles()
		item = article()

		item["title"] = response.meta["title"]
		p = response.css('#main .intro')[0]
		item["paragraph"] = f"{p.xpath('string(//p[1])').getall()[0]}"
		items["link"] = response.meta["link"]
		items["body"] = item
		return items