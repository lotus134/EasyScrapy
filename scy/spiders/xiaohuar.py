import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
class XiaohuarSpider(scrapy.Spider):
    name = "xiaohuar"
    allowed_domains = ["xiaohuar.com"]
    start_urls = ['http://www.xiaohuar.com/list-1-0.html']
    visited_set = set()

    def parse(self, response):
        self.visited_set.add(response.url)
        # 1. 当前页面的所有校花爬下来
        # 获取div并且属性为 class=item masonry_brick
        hxs = HtmlXPathSelector(response)
        item_list = hxs.select('//div[@class="item masonry_brick"]')
        for item in item_list:
            v = item.select('.//span[@class="price"]/text()').extract_first()
            print(v)

        # 2. 在当前页中获取 http://www.xiaohuar.com/list-1-\d+.html，
        # page_list = hxs.select('//a[@href="http://www.xiaohuar.com/list-1-1.html"]')
        page_list = hxs.select('//a[re:test(@href,"http://www.xiaohuar.com/list-1-\d+.html")]/@href').extract()
        for url in page_list:

            if url in self.visited_set:
                pass

            else:
                obj = Request(url=url,method='GET',callback=self.parse)
                yield obj
