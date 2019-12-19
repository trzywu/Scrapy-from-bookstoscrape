# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import csv


def productinfo(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()


class BookSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    output = "books.csv"
    row_name = ['Title', 'Price', 'Full_image_url', 'Rating', 'Product_desription', 'UPC', 'Product_type', 'Price_without_tax', 'Price_with_tax', 'Tax','Availability', 'Nr_reviews']
    with open(output, "w", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(row_name)



    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()

        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # getting to next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_url = response.urljoin(next_page_url)
        yield Request(absolute_url)

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        full_image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        product_desription = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        upc = productinfo(response, 'UPC')
        product_type = productinfo(response, 'Product Type')
        price_without_tax = productinfo(response, 'Price (excl. tax)')
        price_with_tax = productinfo(response, 'Price (incl. tax)')
        tax = productinfo(response, 'Tax')
        availability = productinfo(response, 'Availability')
        nr_reviews = productinfo(response, 'Number of reviews')

        with open(self.output, "a", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow([title, price, full_image_url, rating, product_desription, upc, product_type, price_without_tax, price_with_tax, tax,availability, nr_reviews])
 




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
