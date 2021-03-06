# -*- coding: utf-8 -*-
import scrapy
from cnblogs.items import WordItem

class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):
        # Selector选择器  底层是lxml
        # 1. 构建选择器
        sel = scrapy.Selector(response)
        # 2. 开始xpath抓取，得到每一个文章详细的页面的连接
        #//*[@id="post_list"]/div[1]/div[2]/h3/a
        #.extract() 把选择器对象转换为列表形式(lxml节点形式)
        a_href_list = sel.xpath('//*[@id="post_list"]/div/div[2]/h3/a/@href').extract()
        # a_href_list = response.xpath('//*[@id="post_list"]/div/div[2]/h3/a/@href').extract()
        # print(a_href_list)
        # 3. 将链接使用requests发送请求，交给新的方法进行处理
        for url in a_href_list:
            print('*' * 50, url)
            yield scrapy.Request(url=url, callback=self.parse_info)
        # 4. 处理下一页
        # （1） 得到next的href
        #//*[@id="paging_block"]/div/a[12]
        # 得到最后一个标签last()
        next_ele = sel.xpath('//*[@id="paging_block"]/div/a[last()]')
        # next_test = sel.xpath('//*[@id="paging_block"]/div/a[last()]/text()').extract()[0]
        # next_href = sel.xpath('//*[@id="paging_block"]/div/a[last()]/@href').extract()[0]
        if next_ele: #判断节点是否能得到
            next_text = next_ele.xpath('text()').extract()[0]
            if next_text == 'Next >':
                next_href = next_ele.xpath('@href').extract()[0]
                print('*' * 100, next_href)
                # 可以把下一页交给自身做处理
                # 发送请求
                # url   请求地址
                # callback      请求经过下载器下载生成的response，然后执行处理的方法
                # （2）修复链接
                # yield scrapy.Request(url="http://www.cnblogs.com" + next_href,callback=self.parse)
                yield scrapy.Request(url=response.urljoin(next_href),callback=self.parse)

    def parse_info(self, response):
        print(">" * 100, response.url)
        # 标题
        #//*[@id="cb_post_title_url"]
        title = response.xpath('//*[@id="cb_post_title_url"]/text()').extract()[0]
        # 内容
        #//div[@class="postBody"]
        # 方法一，只能得到文字，不能得到图片
        body = response.xpath('string(//div[@class="postBody"])').extract()[0]
        # 方法二，能得到div下面所有的内容
        # body = response.xspath('//div[@class="postBody"]').extract()[0]
        # print("*" * 100)
        # print(body.len)
        # print(body)

        item = WordItem()
        item['title'] = title
        item['body'] = body
        yield item
