# -*- coding: UTF-8 -*-
# @Time       : 2018/10/21 17:14
# @Author     : Weiqiang.long
# @File       : add_guest_test.py
# @Software   : PyCharm
# @Description: 
# @TODO       :

import unittest
from HTMLTestRunnerPY3 import HTMLTestRunner
import os
import requests
import time

class Add_guest_test(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/add_guest/'
        self.headers = {'Content-Type': 'application/json'}

    def test_request_method_error(self):
        '''请求方式错误'''
        r = requests.get(self.url, headers=self.headers)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 100)
        # 判断message
        self.assertEqual(ruselt['message'], '请求方式有误')

    def test_parameter_null(self):
        '''请求参数的字段为空'''
        data = {"event_id": "", "realname": ""}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 500)
        # 判断message
        self.assertEqual(ruselt['message'], '字段不能为空')

    def test_parameters_null(self):
        '''所有请求参数为空'''
        data = {"event_id": "", "realname": "", "phone": "", "email": "", "sign": ""}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 101)
        # 判断message
        self.assertEqual(ruselt['message'], '请求参数为空')

    def test_event_id_not_int(self):
        '''event_id参数为非整型'''
        data = {"event_id": "qwe", "realname": "测试嘉宾", "phone": "1234567", "email": "1234567@qq.com", "sign": "1"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 102)
        # 判断message
        self.assertEqual(ruselt['message'], 'event_id参数类型有误')

    def test_event_id_not_in_guest_list(self):
        '''event_id不存在'''
        # 使用时间戳作为发布会id
        eid = int(time.time())
        data = {"event_id": eid, "realname": "测试嘉宾", "phone": "1234567", "email": "1234567@qq.com", "sign": "1"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 103)
        # 判断message
        self.assertEqual(ruselt['message'], '发布会id不存在')

    def test_sign_null(self):
        '''sign参数类型为非整型'''
        data = {"event_id": 1, "realname": "测试嘉宾", "phone": "1234567", "email": "1234567@qq.com", "sign": "qwe"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 104)
        # 判断message
        self.assertEqual(ruselt['message'], 'sign参数类型有误')

    def test_sign_not_0_1(self):
        '''sign参数不等于0或1'''
        data = {"event_id": 1, "realname": "测试嘉宾", "phone": "1234567", "email": "1234567@qq.com", "sign": 2}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 105)
        # 判断message
        self.assertEqual(ruselt['message'], 'sign参数只能为0或1')

    def test_phone_equal(self):
        '''手机号重复'''
        data = {"event_id": 1, "realname": "测试嘉宾", "phone": "18888888888", "email": "1234567@qq.com", "sign": 1}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 106)
        # 判断message
        self.assertEqual(ruselt['message'], '手机号已存在')

    @unittest.skip("此用例只执行一次")
    def test_add_guest(self):
        '''添加嘉宾成功'''
        data = {"event_id": 1, "realname": "测试嘉宾", "phone": "10000000000", "email": "1234567@qq.com", "sign": 1}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 200)
        # 判断message
        self.assertEqual(ruselt['message'], '新增嘉宾成功')












# def casesuite():
#     suite = unittest.TestSuite()
#     suite.addTest(Add_guest_test("test_request_method_error"))
#     # suite.addTest(Get_guest_test("test_guest_error"))
#     unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    unittest.main()