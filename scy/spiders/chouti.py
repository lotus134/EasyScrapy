import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

class DigSpider(scrapy.Spider):
    # 爬虫应用的名称，通过此名称启动爬虫命令
    name = "dig"

    # 允许的域名
    allowed_domains = ["chouti.com"]

    # 起始URL
    start_urls = [
        'https://dig.chouti.com/all/hot/recent/1',
    ]

    visited_set = set()

    def parse(self, response):
        self.visited_set.add(response.url)
        # 1. 当前页面的所有chouti爬下来
        # 获取div并且属性为 class=item
        hxs = HtmlXPathSelector(response)
        item_list = hxs.select('//div[@class="item"]')
        for item in item_list:
            v = item.select('.//a[@class="show-content color-chag"]/text()').extract_first()
            print(v)
            print(11212)

        # 2. 在当前页中获取 https://dig.chouti.com/all/hot/recent/1，
        page_list = hxs.select('//a[re:test(@href,"/all/hot/recent/\d+")]/@href').extract()
        for url in page_list:
            url = "https://dig.chouti.com"+url

            if url in self.visited_set:
                pass
            else:
                obj = Request(url=url, method='GET', callback=self.parse)
                yield obj

