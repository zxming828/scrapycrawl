# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import json
from scrapy import signals
from scrapy.exporters import XmlItemExporter

class CaipiaoPipeline(object):
    def process_item(self, item, spider):
        logging.debug('----CaipiaoPipeline----')
        if item['date']:
            item['date'] = item['date'] + '.Num'

        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('/home/CORPUSERS/xp017845/zxmcrawl/caipiao/items.json', 'wb')

    def process_item(self, item, spider):
        logging.debug('----JsonWriterPipeline----')
        self.file.write(str(item))
        self.file.write('\n')
        return item

class XmlExportPipeline(object):

    def __init__(self):
        self.file = open('/home/CORPUSERS/xp017845/zxmcrawl/caipiao/cp_products.xml', 'w+b')
        self.exporter = XmlItemExporter(self.file, item_element='item', root_element='root')
    '''
    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline
    '''

    def open_spider(self, spider):
        logging.debug('----open_spider----')
        #file = open('/home/CORPUSERS/xp017845/zxmcrawl/caipiao/%s_products.xml' % spider.name, 'w+b')
        #self.files[spider] = file
        #self.exporter = XmlItemExporter(file)
        #XmlItemExporter(file, item_element='item', root_element='items')
        #self.exporter = XmlItemExporter(self.file, item_element='item', root_element='root')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        logging.debug('----close_spider----')
        self.exporter.finish_exporting()
        #file = self.file.pop(spider)
        self.file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
