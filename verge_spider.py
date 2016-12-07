import scrapy

from tutorial.items import *

class VergeSpider(scrapy.Spider):
    name = "verge"
    allowed_domains = ["theverge.com"]
    start_urls = [
        "http://www.theverge.com/reviews",
        "http://www.theverge.com/tech/archives",
        "http://www.theverge.com/circuitbreaker/archives",
        "http://www.theverge.com/science/archives",
        "http://www.theverge.com/entertainment/archives",
        "http://www.theverge.com/transportation/archives",
        "http://www.theverge.com/tldr/archives",
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="body"]/h3/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
        item = VergeItem()

        #pulls tags
        item['category'] = response.xpath('//ul[contains(@class, "p-entry-header__labels")]/li/a/text()').extract()

        #word count
        item['body'] = str(response.xpath('//p/text()').extract())
        item['body'] = len(item['body'].split(" "))

        item['url'] = response.url

        item['byline'] = []
        #pulls byline
        text = response.xpath('//a[contains(@class, "author fn")]/text()').extract()

        #converts to string and removes extra characters
        text = str(text)
        text = text.translate(None, '[],')
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
