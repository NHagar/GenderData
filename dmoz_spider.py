import scrapy

from tutorial.items import *

class VergeSpider(scrapy.Spider):
    name = "wired"
    allowed_domains = ["wired.com"]
    start_urls = [
        "http://www.wired.com/category/business/",
        "http://www.wired.com/category/culture/",
        "http://www.wired.com/category/design/",
        "http://www.wired.com/category/gear/",
        "http://www.wired.com/category/science/",
        "https://www.wired.com/category/security/",
        "https://www.wired.com/category/transportation/",
    ]

    #defines spider
    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "clearfix pad")]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    #def parse_dir_contents(self, response):
    def parse_dir_contents(self, response):
        item = VergeItem()
        item['url'] = response.url

        item['category'] = response.xpath('//li[contains(@class, "no-underline pad-t-med pad-r-sm no-marg")]/a/text()').extract()

        #grabs word count
        item['body'] = str(response.xpath('//article/p/text()').extract())
        item['body'] = len(item['body'].split(" "))

        item['byline'] = []
        #pulls byline
        text = response.xpath('//span[contains(@class, "link-underline-sm marg-r-sm")]/a/text()').extract()

        #converts to string and removes extra characters
        text = str(text)
        text = text.translate(None, '[],')
        text = text.replace("'", "", 2)
        text = text.replace("u", "", 1)

        ##accounts for variance in bylines
        if text == "":
            text = response.xpath('//span[contains(@class, "link-underline-sm marg-r-sm")]/text()').extract()
            #converts to string and removes extra characters
            text = str(text)
            text = text.translate(None, '[]\,')
            text = text.replace("'", "", 2)
            text = text.replace("u", "", 1)
            text = text.replace(text[0:4], "")
            text = text.replace(text[-2:-1], "")

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

        #Moves spider to next page
        #for href in response.xpath('//div[@class="card text med-order-1 med-col-18 big-col-9 col mob-pad"]/a/@href'):
        #    url = response.urljoin(href.extract())
        #    yield scrapy.Request(url, self.parse_dir_contents)

        #next_page = response.xpath('//div[@class="card text med-order-1 med-col-18 big-col-9 col mob-pad"]/a/@href')
        #if next_page:
        #    url = response.urljoin(next_page[0].extract())
        #    yield scrapy.Request(url, self.parse_dir_contents)
