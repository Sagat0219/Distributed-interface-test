# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from scrapy import signals
from .func import constants as cs
import logging
import pymysql

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

DB = pymysql.connect('IP address', 'username', 'password', 'Interfacetest', charset='utf8', port=3306)

class XlstestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        spider.logger.info("-------------- Execute TestCases ---------------")  #开始执行标记行

    def spider_closed(self,spider):
        spider.logger.info("--------------- Get the result ----------------- %s", cs.EXEC_RESULT)   #记录最终执行结果（只要有一行失败则失败）
        cs.FailResults.align["Number"] = "l"    #字段的水平对齐方式(左对齐)
        cs.FailResults.padding_width = 1    #列数据左右的空格数量
        spider.logger.info("FailureInfo")
        spider.logger.info('\n'+cs.FailResults.get_string(sortby="Number")) #输出执行失败的行表(按Number字段排序)
        DB.close()

class XlstestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#自定义下载中间件脚本
class HttpbinMiddleware():
    
    def process_response(self, request, response, spider):
        testNumber = int(request.meta.get('testNumber', 1))  #用例编号
        expectCode = int(float(request.meta.get('testCode', 1)))    #预期值
        actualCode = int(response.status)   #获取返回状态代码

        result = True
        if actualCode == expectCode:
            logger.info("Number %s", testNumber)
            logger.info("Result %s", 'PASS')
        else:
            result = False
            cs.EXEC_RESULT = False
            #添加失败的用例信息到结果表(全部执行完最后输出到日志)
            cs.FailResults.add_row([testNumber,request.url,actualCode,expectCode])
            logger.info("FailCase %s", testNumber)

        #将所有执行结果记录到本地Mysql数据库
        sql = 'insert into testresult(TestNumber, URL, ActualCode, ExpectCode, Result) values(%s,%s,%s,%s,%s)'
        cursor = DB.cursor()
        cursor.execute(sql,(testNumber, request.url, actualCode, expectCode, result))
        DB.commit()

        return response
