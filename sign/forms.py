# -*- coding: UTF-8 -*-
# @Time       : 2018/9/8 11:32
# @Author     : Weiqiang.long
# @File       : forms.py
# @Software   : PyCharm
# @Description: 
# @TODO       : 表单提交

from django import forms
from django.forms import ModelForm
from sign.models import Guest, Event


# 添加发布会表单
class AddEventForm(forms.Form):
    name = forms.CharField(max_length=100)  # 发布会标题
    limit = forms.IntegerField()    # 发布会人数
    status = forms.BooleanField(required=False) # 状态(默认false)
    address = forms.CharField(max_length=200)   # 地址
    start_time = forms.DateTimeField()  # 发布会时间



# 添加嘉宾表单
class AddGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['event', 'realname', 'phone', 'email', 'sign']