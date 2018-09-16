# -*- coding: UTF-8 -*-
# @Time       : 2018/9/16 17:07
# @Author     : Weiqiang.long
# @File       : urls.py
# @Software   : PyCharm
# @Description: 
# @TODO       :

from django.urls import path
from sign import views_api

urlpatterns = [
    path('get_event_list/', views_api.get_event_list),
    path('add_event/', views_api.add_event),
    path('get_guest_list/', views_api.get_guest_list),
    path('add_guest/', views_api.add_guest),
    path('user_sign/', views_api.user_sign),




]


