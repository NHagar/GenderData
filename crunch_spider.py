import scrapy

from tutorial.items import *

class VergeSpider(scrapy.Spider):
    name = "tech"
    allowed_domains = ["techcrunch.com"]
    start_urls = [
        "http://techcrunch.com/startups/",
        "http://techcrunch.com/mobile/",
        "http://techcrunch.com/gadgets/",
        "http://techcrunch.com/enterprise/",
        "http://techcrunch.com/social/",
    ]

    def parse(self, response):
        for href in response.xpath('//h2/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        item = VergeItem()

        category = response.xpath('//div[@class="loaded acc-handle"]/a/text()').extract()
        category = str(category)
        category = category.translate(None, '[]\,')
        category = category.replace("'", "")
        category = category.replace("u", "", 1)
        category = category.replace(category[0:8], "")
        category = category.replace(category[-7:-1], "")
        item['category'] = category

        #word count
        item['body'] = str(response.xpath('//div[@class="article-entry text"]/p/text()').extract())
        item['body'] = len(item['body'].split(" "))

        item['url'] = response.url

        item['byline'] = []
        #pulls byline
        text = response.xpath('//div[@class="byline"]/a/text()').extract()

        #converts to string and removes extra characters
        text = str(text)
        text = text.translate(None, '[]\,')
        text = text.replace("'", "", 2)
        text = text.replace("u", "", 1)

        #opens files
        male = open('mwriters')
        female = open('wwriters')

        #looks for names in databases and assigns classification
        for line in male:
            if text in line:
                item['byline'] = "m"

        for line in female:
            if text in line:
                item['byline'] = "w"

        #freelance classification
        if item['byline'] == []:
            item['byline'] = text

        #spits out to spreadsheet
        yield item
