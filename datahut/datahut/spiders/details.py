# Import necessary modules
import scrapy
from datahut.items import Carbon38ScraperItem

class Carbon38Spider(scrapy.Spider):
    name = 'carbon38'
    start_urls = ['https://www.carbon38.com/shop-all-activewear/tops']

    def parse(self, response):
        # Extract links to individual product pages
        product_links = response.xpath('h2.ProductItem__Title.Heading a::attr(href)').extract()
        for product_link in product_links:
            print(product_link)
            yield scrapy.Request(url=product_link, callback=self.parse_product)

        # Follow pagination links
    #     next_page = response.xpath('//a[@class="next"]/@href').extract_first()
    #     if next_page:
    #         yield scrapy.Request(url=next_page, callback=self.parse)

    # def parse_product(self, response):
    #     item = Carbon38ScraperItem()

    #     # Extracting required fields
    #     item['breadcrumbs'] = response.xpath('//div[@class="breadcrumbs"]/a/text()').extract()
    #     item['image_url'] = response.xpath('//img[@class="product-image-photo"]/@src').extract_first()
    #     item['brand'] = response.xpath('//div[@class="brand"]/a/text()').extract_first()
    #     item['product_name'] = response.xpath('//h1[@class="product-name"]/text()').extract_first()
    #     item['price'] = response.xpath('//span[@class="price"]/text()').extract_first()
    #     item['reviews'] = response.xpath('//div[@class="rating-summary"]/span[@class="label"]/text()').extract_first()
    #     item['colour'] = response.xpath('//div[@class="product-attribute-color"]/div[@class="value"]/text()').extract_first()
    #     item['sizes'] = response.xpath('//div[@class="product-options"]/div[@class="swatch-attribute-options size"]/div/text()').extract()
    #     item['description'] = ' '.join(response.xpath('//div[@class="product attribute description"]/div[@class="value"]/p/text()').extract())
    #     item['sku'] = response.xpath('//div[@class="product attribute sku"]/div[@class="value"]/text()').extract_first()
    #     item['product_id'] = response.xpath('//div[@class="product attribute product-id"]/div[@class="value"]/text()').extract_first()

    #     yield item
