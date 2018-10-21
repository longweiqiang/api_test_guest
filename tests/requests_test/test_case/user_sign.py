# -*- coding: UTF-8 -*-
# @Time       : 2018/10/21 21:07
# @Author     : Weiqiang.long
# @File       : user_sign.py
# @Software   : PyCharm
# @Description: 
# @TODO       :

import unittest
import requests
import time

class Uesr_sign_test(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/user_sign/'
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
        data = {" ": "", "": ""}
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
        '''请求参数为空'''
        data = {"id": "", "phone": ""}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 101)
        # 判断message
        self.assertEqual(ruselt['message'], '请求参数为空')

    def test_id_not_int(self):
        '''id类型为非整型'''
        data = {"id": "qwe", "phone": "10000000001"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 102)
        # 判断message
        self.assertEqual(ruselt['message'], '发布会id参数类型有误')

    def test_phont_len(self):
        '''手机号长度大于11位'''
        data = {"id": 1, "phone": "100000000011"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 103)
        # 判断message
        self.assertEqual(ruselt['message'], '手机号长度有误')

    def test_id_not_exist(self):
        '''发布会id不存在'''
        # 使用时间戳作为发布会id
        eid = int(time.time())
        data = {"id": eid, "phone": "10000000001"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 104)
        # 判断message
        self.assertEqual(ruselt['message'], '发布会id不存在')

    def test_event_status_is_false(self):
        '''发布会状态未开启'''
        data = {"id": 7, "phone": "10000000001"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 105)
        # 判断message
        self.assertEqual(ruselt['message'], '发布会未开启，不能签到')

    def test_event_outmoded(self):
        '''发布会已过期'''
        data = {"id": 1, "phone": "10000000001"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 106)
        # 判断message
        self.assertEqual(ruselt['message'], '发布会已开始，无法签到')

    def test_phone_not_exist(self):
        '''签到手机号不存在'''
        data = {"id": 2, "phone": "10000000002"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 107)
        # 判断message
        self.assertEqual(ruselt['message'], '签到手机号不存在')

    def test_not_join_event(self):
        '''用户没有参加该场发布会'''
        data = {"id": 2, "phone": "10000000000"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 108)
        # 判断message
        self.assertEqual(ruselt['message'], '用户没有参加本场发布会')

    def test_sign_status_repetition(self):
        '''重复签到'''
        data = {"id": 2, "phone": "12222222222"}
        r = requests.post(self.url, headers=self.headers, json=data)
        # print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 109)
        # 判断message
        self.assertEqual(ruselt['message'], '用户已签到，请勿重复签到')

    def test_user_sign(self):
        '''用户签到成功'''
        data = {"id": 2, "phone": "18888888880"}
        r = requests.post(self.url, headers=self.headers, json=data)
        print(r.json())
        ruselt = r.json()
        # 判断http状态码
        self.assertEqual(r.status_code, 200)
        # 判断status
        self.assertEqual(ruselt['status'], 200)
        # 判断message
        self.assertEqual(ruselt['message'], '用户签到成功')




if __name__ == '__main__':
    unittest.main()









