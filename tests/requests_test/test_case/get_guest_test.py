# -*- coding: UTF-8 -*-
# @Time       : 2018/10/21 16:03
# @Author     : Weiqiang.long
# @File       : get_guest_test.py
# @Software   : PyCharm
# @Description: 
# @TODO       :


import unittest
import requests
import os
from HTMLTestRunnerPY3 import HTMLTestRunner


class Get_guest_test(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    def test_guest_success(self):
        '''请求成功'''
        r = requests.get(self.url)
        ruselt = r.json()
        # print(result)
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断自定义状态码
        self.assertEqual(ruselt["status"], 200)
        # 判断message
        self.assertEqual(ruselt["message"], "请求成功")
        # 判断data.name
        self.assertEqual(ruselt["data"][0]["name"], "小米8发布会")

    def test_guest_error(self):
        '''请求失败'''
        r = requests.post(self.url)
        # print(r.json())
        ruselt = r.json()
        # 判断自定义状态码
        self.assertEqual(ruselt["status"], 100)
        # 判断message
        self.assertEqual(ruselt["message"], "请求方式有误")

# def casesuite():
#     suite = unittest.TestSuite()
#     suite.addTest(Get_guest_test("test_guest_success"))
#     suite.addTest(Get_guest_test("test_guest_error"))
#     unittest.TextTestRunner().run(suite)





if __name__ == '__main__':
    # 当前文件的路径
    pwd = os.getcwd()
    # 当前文件的父路径
    # father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    # 定义报告存放路径
    report_file = pwd + "\\report\\report.html"

    report_title = '发布会接口测试执行报告'
    desc = 'django项目接口测试'

    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(Get_guest_test))

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report, title=report_title, description=desc)
        runner.run(testsuite)













