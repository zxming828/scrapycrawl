# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from caipiao.items import SSQItem, DLTItem
from scrapy import log

import logging
import json

class CaipiaoSpider(Spider):
    name = "caipiao"
    start_urls = [
        "http://baidu.lecai.com/lottery/draw/?agentId=5571"
    ]

    def parse(self, response):
        sel = Selector(response)
        kj_box = sel.xpath('//div[@class="kj_box"]')
        #title = kj_box.xpath('./h1/text()').extract()
        kj_tab = kj_box.xpath('./table[@class="kj_tab"]')
        lottery_info = kj_tab.xpath('./tr')
        for info in lottery_info:
            try:
                lottery_name = info.xpath('./td')[0].xpath('./a/text()').extract()[0]
                lottery_link = info.xpath('./td')[0].xpath('./a/@href').extract()[0]
                if lottery_name == u"双色球":
                   full_url = response.urljoin(lottery_link)
                   self.log("=====in=====")
                   yield scrapy.Request(full_url, callback=self.parse_ssq)
                else:
                   self.log("=====not=====")
            except Exception, e:
                self.log("=====exception=====")


        '''
        ssq_item = SSQItem()
        dlt_item = DLTItem()

        ballbg = kj_box.xpath('//div[@class="ballbg"]')

        #ball_number = ballbg[0].xpath('./span[@class="ball_1"]/text()').extract()
        self.log("start=========")
        #logging.debug(ball_numbe# r)


        for lottery in ballbg:
            lottery_name = lottery.xpath('./td')[0].xpath('./text()').extract()
            self.log(lottery_name)
            #ball_number = lottery.xpath('./span[@class="ball_1"]/text()').extract()

        self.log("end=========")

        #ball = ballbg.xpath('./span[@class="ball_1"]/text()').extract()
        '''

    def parse_ssq(self, response):
        self.log("=====parse_ssq=====")
        self.log(response.url)
        sel = Selector(response)
        date = sel.xpath('//div[@class="sl-draw-sell"]')
        day = date.xpath('./select/option[@selected="selected"]/text()').extract()[0]

        tmp = int(day)
        start = int(day[:4]+"001")
        self.log(tmp)
        self.log(start)

        while tmp >= 2017037:
            tmp_url = 'http://baidu.lecai.com/lottery/draw/ajax_get_detail.php?lottery_type=50&phase='
            full_url = tmp_url + str(tmp)
            tmp -= 1
            yield scrapy.Request(full_url, callback=self.parse_json)

        '''
        if tmp >= 2017035:
            ssq_item = SSQItem()
            ssq_item['date'] = tmp
            ssq_item['red'] = sel.xpath('//ul/li[@class="red"]')
            ssq_item['blue'] = sel.xpath('//ul/li[@class="blue"]')

            yield ssq_item

            tmp = tmp - 1
            tmp_url = 'http://baidu.lecai.com/lottery/draw/ajax_get_detail.php?lottery_type=50&phase='
            full_url = tmp_url + str(tmp)

            yield scrapy.Request(full_url, callback=self.parse_json)

        else:
            self.log("=====end=====")
        '''


        self.log("=====parse_end=====")

    def parse_json(self, response):

        self.log("=====parse_json=====")
        sites = json.loads(response.body_as_unicode())
        ssq_item = SSQItem()
        ssq_item['date'] = sites['data']['phase']
        for ball in sites['data']['result']['result']:
            if ball['key'] == 'red':
                ssq_item['red'] = ball['data']
            if ball['key'] == 'blue':
                ssq_item['blue'] = ball['data']
        yield ssq_item


