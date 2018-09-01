from django.contrib import admin
from sign.models import Guest, Event

# Register your models here.

# 把模型映射到admin后台
#增加发布会列表
class EventAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['name','id','status','start_time']
    # 搜索功能
    search_fields = ['name']
    # 过滤器
    list_filter = ['status']


# 增加嘉宾列表
class GuestAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['realname','id','phone','email','sign','create_time','event_id']
    # 显示链接
    list_display_links = ('realname','phone')
    # 搜索功能
    search_fields = ['realname', 'phone']
    # 过滤器
    list_filter = ['event_id']




admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
