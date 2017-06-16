import scrapy
import re
import json


class OrsaySpider(scrapy.Spider):
    name = 'orsay'

    start_urls = [
        'http://www.orsay.com/de-de/shoulder-cut-out-top-10306898.html']

    def parse(self, response):
        f = open('orsay.json', 'w')
        sizes = list(filter(None, [n.strip() for n in response.css(
            'div.sizebox-wrapper li::text ').extract()]))
        avail = response.xpath(
            "//div[@class='sizebox-wrapper']//li/@data-qty").extract()
        data = {
            'brand': "",
            'care': "",
            'description': "",
            'image_urls': "",
            'name': "",
            'retailer_sku': "",
            'urls-color': "",
            'skus': []
        }
        data['brand'] = response.xpath(
            "//script[@type='application/ld+json']/text()").re(r'Brand.*name":"(\w*)"},')[0]
        data['care'] = response.xpath(
            "//div[@class='product-care six columns']//@src | //p[@class='material']/text()").extract()
        data['description'] = str(response.xpath(
            "//p[@class='description']/text()").extract()[0]).strip()
        data['image_urls'] = response.xpath(
            "//div[@class='product-image-gallery-thumbs configurable']//@href").extract()
        data['name'] = response.css("h1.product-name::text").extract()
        data['url-colors'] = [n.strip() for n in response.xpath(
            "//ul[@class='product-colors']//a/@href").extract() if n != '#']
        data['retailer_sku'] = list(filter(None, response.css(
            "p.sku::text").re(r'(\d*)')))[0]
        for s in range(len(sizes)):
            if int(avail[s]):
                data['skus'].append({str(list(filter(None, response.css(
                    "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes[s]):
                    {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                     'currency': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0], 'price': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0], 'size': sizes[s]}})
            else:
                data['skus'].append({str(list(filter(None, response.css(
                    "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes[s]):
                    {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                     'currency': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0], 'price': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0], 'size': sizes[s], 'out_of_stock': 'true'}})

        json.dump(data, f)
