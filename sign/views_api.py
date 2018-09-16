# -*- coding: UTF-8 -*-
# @Time       : 2018/9/16 17:05
# @Author     : Weiqiang.long
# @File       : views_api.py
# @Software   : PyCharm
# @Description: 
# @TODO       :
import json

import time
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from sign.models import Event, Guest


def get_event_list(request):
    """
    获取发布会列表
    :param request:
    :return: 
    """
    if request.method == "GET":

        # 查询所有发布会
        events = Event.objects.all()

        event_list = []
        for event in events:
            # 循环event，并组装到字典中
            event_dict = {
                "id":event.id,
                "name":event.name,
                "limit":event.limit,
                "status":event.status,
                "address":event.address,
                "start_time":event.start_time,
                "create_time":event.create_time
            }

            # 将字典添加到数组中
            event_list.append(event_dict)

        data = {"status":200, "message":"请求成功", "data":event_list}

        return JsonResponse(data)
    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def add_event(requset):
    """
    添加发布会
    :param requset: name, limit, status, address, start_time
    :return: 
    """
    if requset.method == "POST":
        # # 获取前端以form表单方式传的参数
        # name = requset.POST.get("name", "")
        # limit = requset.POST.get("limit", "")
        # status = requset.POST.get("status", "")
        # address = requset.POST.get("address", "")
        # start_time = requset.POST.get("start_time", "")


        # 获取前端以json方式传的参数
        event_dict = json.loads(requset.body)

        name = event_dict["name"]
        limit = event_dict["limit"]
        status = event_dict["status"]
        address = event_dict["address"]
        start_time = event_dict["start_time"]


        # 对各个字段进行空字符串判断，并返回给前台
        if name == "" or limit == "" or address == "" or start_time == "":
            return JsonResponse({"status":101, "message":"请求参数为空"})

        # 对status字段做空字符串判断，如果为真，则默认status=0
        if status == "":
            status = 0

        # 根据入参的name和数据库中的name进行模糊比对，如相同，则返回相应的错误信息
        event = Event.objects.filter(name=name)
        # 如果name相同
        if event:
            return JsonResponse({"status":102, "message":"发布会名称已存在"})

        try:
            # 新增一条发布会信息
            Event.objects.create(name=name, limit=limit, status=status, address=address,
                                 start_time=start_time)
        except ValidationError:
            # 对入参的时间格式进行校验，如格式有误，则抛出相应的错误
            error = "日期格式错误, 请参照:YYYY-MM-DD HH:MM:SS"
            return JsonResponse({"status":103, "message":error})

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "message":"新增发布会成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})


def get_guest_list(request):
    """
    获取嘉宾列表
    :param request:
    :return: 
    """
    if request.method == "GET":

        # 查询所有发布会
        guests = Guest.objects.all()

        guest_list = []
        for guest in guests:
            # 循环event，并组装到字典中
            guest_dict = {
                "id":guest.id,
                "event_id":guest.event_id,
                "realname":guest.realname,
                "phone":guest.phone,
                "email":guest.email,
                "sign":guest.sign,
                "create_time":guest.create_time
            }

            # 将字典添加到数组中
            guest_list.append(guest_dict)

        data = {"status":200, "message":"请求成功", "data":guest_list}

        return JsonResponse(data)
    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def add_guest(request):
    """
    添加嘉宾
    :param requset: event_id, realname, phone, email, sign
    :return: 
    """
    if request.method == "POST":
        # # 获取前端以form表单方式传的参数
        # event_id = requset.POST.get("event_id", "")
        # realname = requset.POST.get("realname", "")
        # phone = requset.POST.get("phone", "")
        # email = requset.POST.get("email", "")
        # sign = requset.POST.get("sign", "")


        # 获取前端以json方式传的参数
        guest_dict = json.loads(request.body)

        event_id = guest_dict["event_id"]
        realname = guest_dict["realname"]
        phone = guest_dict["phone"]
        email = guest_dict["email"]
        sign = guest_dict["sign"]

        # print(type(event_id))


        # 对各个字段进行空字符串判断，并返回给前台
        if event_id == "" or realname == "" or phone == "" or email == "":
            return JsonResponse({"status":101, "message":"请求参数为空"})

        # 对event_id字段的类型进行判断，必须传整型
        if type(event_id) != int:
            return JsonResponse({"status":102, "message":"event_id参数类型有误"})


        """
        此处需要对入参中的event_id参数进行校验，如果入参event_id的值不能和库中event_id匹配，
        则代表该event_id不存在，无法新增嘉宾
        """
        # 查询所有的发布会
        guests = Guest.objects.all()
        # 定义一个空数组
        guest_list = []
        # 通过for循环拿到所有的id，并添加到数组中
        for guest in guests:
            guest_list.append(guest.id)

        # 判断入参的event_id是否存在于guest_list中，如果不存在，则只需if语句块，返回对应json
        if event_id not in guest_list:
            return JsonResponse({"status":103, "message":"发布会id不存在"})



        # 对sign字段做空字符串判断，如果为真，则默认sign=0
        if sign == "":
            sign = 0

        # 对sign字段的类型进行判断，必须传整型
        if type(sign) != int:
            return JsonResponse({"status":104, "message":"sign参数类型有误"})

        # 对sign字段的数据进行判断，必须传0或1
        """
        注意：此处应该用and
        1. 在纯and语句中，如果每一个表达式都不是假的话，那么返回最后一个，因为需要一直匹配直到最后一个。如果有一个是假，那么返回假
        2. 在纯or语句中，只要有一个表达式不是假的话，那么就返回这个表达式的值。只有所有都是假，才返回假
        3. 在or和and语句比较难表达，总而言之，碰到and就往后匹配，碰到or如果or左边的为真，那么就返回or左边的那个值，如果or左边为假，继续匹配or右边的参数。
        """
        if sign != 0 and sign != 1:
            print(sign)
            return JsonResponse({"status":105, "message":"sign参数只能为0或1"})

        # 根据入参的name和数据库中的name进行模糊比对，如相同，则返回相应的错误信息
        guest = Guest.objects.filter(phone=phone)
        # 如果name相同
        if guest:
            return JsonResponse({"status":106, "message":"手机号已存在"})

        # 新增一条发布会信息
        Guest.objects.create(event_id=event_id, realname=realname, phone=phone, email=email,
                                 sign=sign)

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "message":"新增嘉宾成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})


def user_sign(request):
    """
    发布会签到
    :param request: 
    :return: 
    """
    if request.method == "POST":
        # # 获取前端以form表单方式传的参数
        # id = request.POST.get("id", "")
        # phone = request.POST.get("phone", "")

        # 获取前端以json方式传的参数
        sign_dict = json.loads(request.body)

        id = sign_dict["id"]
        phone = sign_dict["phone"]

        # 对各个字段进行空字符串判断，并返回给前台
        if id == "" or phone == "":
            return JsonResponse({"status":101, "message":"请求参数为空"})

        if type(id) != int:
            return JsonResponse({"status":102, "message":"发布会id参数类型有误"})

        if len(phone) != 11:
            # print(len(phone))
            return JsonResponse({"status":103, "message":"手机号长度有误"})

        # 获取发布会id，并判断id是否存在，如果不存在，则返回
        try:
            result = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return JsonResponse({"status": 104, "message": "发布会id不存在"})

        # 判断发布会status状态值，如果是False，则代表发布会未开启，无法签到
        if result.status is False:
            return JsonResponse({"status": 105, "message": "发布会未开启，不能签到"})

        # 获取发布会时间，并转换成YYY-MM-DD HH:MM:SS格式
        event_time = result.start_time     # 发布会时间
        timeArray = time.strptime(str(event_time), "%Y-%m-%d %H:%M:%S")
        e_time = int(time.mktime(timeArray))

        # 获取当前时间
        now_time = str(time.time())          # 当前时间
        ntime = now_time.split(".")[0]
        n_time = int(ntime)

        # 拿当前时间与发布会时间进行比较，如果当前时间大于等于发布会时间，则返回异常
        if n_time >= e_time:
            return JsonResponse({'status':106,"message":"发布会已开始，无法签到"})

        # 获取用户手机号
        result = Guest.objects.filter(phone=phone)

        # 判断入参的手机号是否存在数据库中
        if not result:
            return JsonResponse({'status':107,"message":"签到手机号不存在"})
        else:
            for res in result:
                if res.event_id == int(id):
                    break
            else:
                return JsonResponse({'status': 108, 'message': '用户没有参加本场发布会'})


        result = Guest.objects.get(event_id=id, phone=phone)

        # 判断用户是否已签到
        if result.sign is True:
            return JsonResponse({'status': 109, 'message': '用户已签到，请勿重复签到'})

        # 如果未签到，则执行签到动作，并返回成功
        else:
            result.sign = True
            result.save()
            return JsonResponse({'status':200,'message':'用户签到成功'})

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})






