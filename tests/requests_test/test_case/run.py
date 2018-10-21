# -*- coding: UTF-8 -*-
# @Time       : 2018/10/21 17:27
# @Author     : Weiqiang.long
# @File       : run.py
# @Software   : PyCharm
# @Description: 
# @TODO       :
import os
import unittest
from HTMLTestRunnerPY3 import HTMLTestRunner
from tests.requests_test.test_case import add_guest_test, get_guest_test, user_sign





if __name__ == '__main__':

    # 定义报告存放路径
    pwd = os.getcwd()
    report_file = pwd + "\\report\\report.html"

    report_title = '发布会接口测试执行报告'
    desc = 'django项目接口测试'

    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(get_guest_test.Get_guest_test))
    testsuite.addTest(unittest.makeSuite(add_guest_test.Add_guest_test))
    testsuite.addTest(unittest.makeSuite(user_sign.Uesr_sign_test))

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report, title=report_title, description=desc)
        runner.run(testsuite)






