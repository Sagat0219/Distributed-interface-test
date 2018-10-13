#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 通用包：常量
from prettytable import PrettyTable

CASE_NUMBER = 0  # 用例编号
CASE_NAME = 1    # 用例名称
CASE_DATA = 2    # 用例参数
CASE_URL = 3     # 用例接口地址
CASE_METHOD = 4  # 用例请求类型
CASE_CODE = 5    # 用例code
CASE_HEADERS = 6 # 用例headers

#用例文件名
FILE_NAME = 'test.xlsx'
#执行完成结果(默认为True)
EXEC_RESULT = True
#记录执行失败的case信息
FailResults = PrettyTable(["Number", "Url", "ActualCode", "ExpectCode"])	#定义结果表的字段头