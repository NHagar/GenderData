import scrapy

from tutorial.items import *

class VergeSpider(scrapy.Spider):
    name = "engadget"
    allowed_domains = ["engadget.com"]
    start_urls = [
            "https://www.engadget.com/gear/",
            "https://www.engadget.com/gaming/",
            "https://www.engadget.com/culture/",
            "https://www.engadget.com/entertainment/",
            "https://www.engadget.com/science/",
            "https://www.engadget.com/reviews/",
    ]

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "o-hit__link")]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = VergeItem()

        item['category'] = response.xpath('//div[@class="mt-5"]/span/a[contains(@class, "th-meta")]/text()').extract()

        #word count
        item['body'] = str(response.xpath('//div[@class="grid@tl+"]/div/div/p/text()').extract())
        item['body'] = len(item['body'].split(" "))

        item['url'] = response.url

        item['byline'] = []
        #pulls byline
        text = response.xpath('//div[@class="t-meta-small@s t-meta@m+"]/a/text()').extract()

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
