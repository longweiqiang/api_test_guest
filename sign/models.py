from django.db import models

# Create your models here.

# 发布会表
class Event(models.Model):
    # 发布会标题
    name = models.CharField("名称", max_length=100)
    # 参加人数
    limit = models.IntegerField("人数")
    # 状态
    status = models.BooleanField("状态")
    # 地址
    address = models.CharField("地址", max_length=200)
    # 发布会时间
    start_time = models.DateTimeField("时间")
    # 创建时间(自动获取当前时间)
    create_time = models.DateTimeField("新增时间", auto_now=True)

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    # 关联发布会id
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # 姓名
    realname = models.CharField("姓名", max_length=64)
    # 手机号
    phone = models.CharField("手机号", max_length=16)
    # 邮箱
    email = models.EmailField("邮箱")
    # 签到状态
    sign = models.BooleanField("签到状态")
    # 创建时间(自动获取当前时间)
    create_time = models.DateTimeField("创建时间", auto_now=True)


