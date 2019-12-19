# -*- coding: utf-8 -*-
from scrapy import  Spider
from scrapy.http import  Request




class BookSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self,response):
        books = response.xpath('//h3/a/@href').extract()

        for book in books:
            absolute_url = response.urljoin(book)
            yield  Request(absolute_url, callback= self.parse_book)


        #getting to next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_url = response.urljoin(next_page_url)
        yield  Request(absolute_url)

    def product_info(response, value):
        return response.xpath('//th[text()="' + value + '"]/following-sibling:td/text()').extract_first()


    def parse_book(self,response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        full_image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        product_desription = response.xpath('//*[@id="product_description"]/following-sibling::p').extract_first()
        # upc = product_info(response,'UPC')
        # product_type = product_info(response,'Product Type')
        # price_without_tax = product_info(response, 'Price (excl. tax)')
        # price_with_tax = product_info(response, 'Price (incl. tax)')
        # Tax = product_info(response, 'Tax')
        # Availability = product_info(response, 'Availability')
        # number_of_review = product_info(response,'Number of reviews')

        yield {
            'title' : title,
            'price' : price,
            'Image_URL' : full_image_url,
            'Ratimg' : rating,
            'Product Descritpion' : product_desription,
            # 'UPC': upc,
            # 'Product Type': product_type,
            # 'Price (excl. tax)' : price_without_tax,
            # 'Price (incl. tax)' : price_with_tax,
            # 'Tax': Tax,
            # 'Availability' : Availability,
            # 'Number of reviews' : number_of_review
        }








# -*- coding: utf-8 -*-
# from scrapy import Spider
# from selenium import webdriver
# from scrapy.selector import Selector
# from scrapy.http import Request
# from time import  sleep
# from selenium.common.exceptions import NoSuchAttributeException
#
#
# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#
#
#     def start_requests(self):
#         self.driver = webdriver.Chrome('/home/admin12/Downloads/chromedriver')
#         self.driver.get('http://books.toscrape.com/')
#
#         sel = Selector(text= self.driver.page_source)
#         books = sel.xpath('//h3/a/@href').extract()
#
#         for book in books:
#             url= 'http://books.toscrape.com/'+ book
#             yield  Request(url,callback=self.parse_book)
#
#         while True:
#             try:
#                 next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
#                 sleep(4)
#                 self.logger.info('3 seconds sleeping!')
#                 next_page.click()
#
#                 sel = Selector(text= self.driver.page_source)
#                 books = sel.xpath('//h3/a/@href').extract()
#
#                 for book in books:
#                     url= 'http://books.toscrape.com/catalogue/'+ book
#                     yield  Request(url,callback=self.parse_book)
#
#             except NoSuchAttributeException:
#                 self.logger.info('No more pages to load')
#                 self.driver.quit()
#                 break
#
#     def parse_book(self,response):
#         pass
#
