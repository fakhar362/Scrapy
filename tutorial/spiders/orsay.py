import scrapy
import re


class OrsaySpider(scrapy.Spider):
    name = 'orsay'

    start_urls = [
        'http://www.orsay.com/de-de/shoulder-cut-out-top-10306897.html']

    def parse(self, response):
        yield {
            'brand': response.xpath(
                "//script[@type='application/ld+json']/text()").re(r'Brand.*name":"(\w*)"},')[0],
            'care': response.xpath("//div[@class='product-care six columns']//@src | //p[@class='material']/text()").extract(),
            'description': response.xpath("//p[@class='description']/text()").extract(),
            'image_urls': response.xpath("//div[@class='product-image-gallery-thumbs configurable']//@href").extract(),
            'name': response.css("h1.product-name::text").extract(),
            'retailer_sku': response.css("p.sku::text").re(r'(\d*)660000')[0],
                'skus': {str(response.css("p.sku::text").re(r'(\d*)660000')[0] + '_' + response.css('div.sizebox-wrapper li[data-optionid="1151"]::text').extract()[0].strip()):
                     {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                      'currency': response.xpath(
                         "//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0], 'price': response.xpath(
                         "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0], 'size': response.css('div.sizebox-wrapper li[data-optionid="1151"]::text').extract()[0].strip()}},
            'size': list(filter(None, [n.strip() for n in response.css('div.sizebox-wrapper li::text').extract()])),
            'test': response.xpath(
                "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0]
        }

    def parse_skus(self, response):
        def extract_with_css(query):
            return response.css(query)

        yield {
            'color': extract_with_css('h1.product-name::text'),
            'currency': extract_with_css('h1.product-name::text'),
            'price': extract_with_css('h1.product-name::text'),
            'size': extract_with_css('h1.product-name::text'),
        }
