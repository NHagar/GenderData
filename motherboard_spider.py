import scrapy

from tutorial.items import *

class VergeSpider(scrapy.Spider):
    name = "motherboard"
    allowed_domains = ["vice.com"]
    start_urls = [
          "http://motherboard.vice.com/en_us/tag/machines?trk_source=nav",
          "http://motherboard.vice.com/en_us/tag/discoveries?trk_source=nav",
          "http://motherboard.vice.com/en_us/tag/space?trk_source=nav",
          "http://motherboard.vice.com/en_us/tag/futures?trk_source=nav",
          "http://motherboard.vice.com/en_us/tag/gaming?trk_source=nav",
          "http://motherboard.vice.com/en_us/tag/earth?trk_source=nav",
    ]

    def parse(self, response):
        for href in response.xpath('//h3/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = VergeItem()

        item['category'] = response.xpath('//span[contains(@class, "tag")]/a/text()').extract()
        
        #word count
        item['body'] = str(response.xpath('//div[@class="article-content rich-text"]/p/text()').extract())
        item['body'] = len(item['body'].split(" "))

        item['url'] = response.url

        item['byline'] = []
        #pulls byline
        text = response.xpath('//section[contains(@class, "motherboard-portlet motherboard-portlet-about")]/div/h3/a/text()').extract()

        #converts to string and removes extra characters
        text = str(text)
        text = text.translate(None, '[],')
        text = text.replace("'", "", 2)
        text = text.replace("u", "", 1)

        if text == "":
            text = response.xpath('//section[contains(@class, "motherboard-portlet motherboard-portlet-about")]/div/h3/text()').extract()
            #converts to string and removes extra characters
            text = str(text)
            text = text.translate(None, '[]\,')
            text = text.replace("'", "", 2)
            text = text.replace("u", "", 1)
#            text = text.replace(text[0:4], "")
#            text = text.replace(text[-2:-1], "")

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
