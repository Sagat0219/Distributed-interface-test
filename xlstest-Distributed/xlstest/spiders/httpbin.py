# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy import Request,FormRequest
from xlstest.func import excel
from xlstest.func import constants as cs
import os
import zipfile


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']

    def start_requests(self):
        base_url = 'http://httpbin.org'
        module = 'user' #sheet name
        file_name = cs.FILE_NAME #用例文件名

        #eggfile = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'case',file_name) #读到路径也不能直接读取egg中的文件
        eggpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #获取临时蛋文件的位置
        zipf = zipfile.ZipFile(eggpath)
        zipf.extract('xlstest/case/'+file_name,'/') #将蛋文件中的测试用例xlsx拷贝到根目录（会连同路径一起拷贝）
        path = '/xlstest/case/' + file_name #获取拷贝出来的测试用例xlsx

        #读取xlsx文件
        excel.open_excel(path)
        sheet = excel.get_sheet(module)
        rows = excel.get_rows(sheet)

        #逐行获取用例的相关请求信息
        for i in range(2,rows):
            testNumber = excel.get_content(sheet, i, cs.CASE_NUMBER)    #用例编号
            testName = excel.get_content(sheet, i, cs.CASE_NAME)    #用例名称
            testUrl = excel.get_content(sheet, i, cs.CASE_URL)  #用例接口地址
            testUrl = base_url + testUrl
            testMethod = excel.get_content(sheet, i, cs.CASE_METHOD)    #用例请求类型
            testMethod = testMethod.strip().upper() #去前后空格并转大写
            testdata = excel.get_content(sheet,i,cs.CASE_DATA)  #用例参数
            testdata = {} if testdata.strip() == '' else eval(testdata)  #为空时转为空字典
            testHeaders = eval(excel.get_content(sheet, i, cs.CASE_HEADERS))
            testCode = str(excel.get_content(sheet, i, cs.CASE_CODE))   #预期值
            #判断请求类型并放入队列
            if testMethod == 'POST':
                yield FormRequest(testUrl, self.parse, headers=testHeaders, formdata=testdata, meta={'testCode': testCode, 'testNumber': testNumber})
            else:
                yield Request(testUrl, self.parse, meta={'testCode': testCode, 'testNumber': testNumber})

    def parse(self, response):
        pass