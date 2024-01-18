import scrapy
import json

class Carbospider(scrapy.Spider):
    name = 'carbonx'
    start_urls = [
        "https://carbon38.com/collections/tops?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/leggings?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/sweaters-knits?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/dresses-jumpsuits?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/jackets-outerwear?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/skirts-shorts?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/all-sneakers?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/flats?filter.v.availability=1&filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/shoes?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/sports-bras?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/collections/new-arrivals?filter.p.m.custom.available_or_waitlist=1",
        "https://carbon38.com/en-in/collections/melt?filter.p.m.custom.available_or_waitlist=1",
    ]

    visited_urls = set()
    def parse(self, response):
        for product in response.css('div.ProductItem__Wrapper'):
            product_link = product.css('h2.ProductItem__Title.Heading a::attr(href)').get()
            if product_link and product_link not in self.visited_urls:
                self.visited_urls.add(product_link)
                yield response.follow(product_link, callback=self.parse_product)
        next_page = response.css('a.Pagination__NavItem[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract details from the product page
        image_url=response.css('div.AspectRatio img::attr(src)').get()
        brand=response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get()
        product_name=response.css('h1.ProductMeta__Title.Heading.u-h3::text').get()
        price=response.css('span.ProductMeta__Price.Price::text').get()
        reviews=response.css('div.yotpo-sr-bottom-line-right-panel div.yotpo-sr-bottom-line-text::text').get()
        colors=response.css('span.ProductForm__SelectedValue::text').get()
        sizes=response.css('ul.SizeSwatchList li input::attr(value)').getall()
        description=response.css('div.Faq__Answer.Rte span[data-mce-fragment="1"]::text').get()
        productid=response.css('input[name="product-id"]::attr(value)').extract_first()
        sku=self.extract_sku(response)
        product_details = {
            'image_url': image_url,
            'brand': brand,
            'product_name': product_name,
            'price': price,
            'reviews': reviews,
            'colors': colors,
            'sizes': sizes,
            'description': description,
            'sku': sku,
            'product_id': productid
        }
        

        product_details['description'] = product_details['description'] if product_details['description'] else 'No description'
        product_details['reviews'] = int(product_details['reviews'].split()[0]) if product_details['reviews'] else '0 Reviews'
        
        yield product_details


    def extract_sku(self, response):
        script_content = response.css('script[data-product-json]::text').get()
        if script_content:
            try:
                product_data = json.loads(script_content)
                variants = product_data.get('product', {}).get('variants', [])
                if variants:
                    return variants[0].get('sku')
            except json.JSONDecodeError:
                self.log("Failed to parse JSON from script tag. Content: %s" % script_content)

        return None