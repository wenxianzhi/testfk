from django.db import models

# Create your models here.
#读书计划表
from django.utils import timezone


class Read(models.Model): #创Read类，继承models.Model
    wd_num = models.CharField(max_length=8)  #工号
    name = models.CharField(max_length=10)  #姓名
    group_name= models.CharField(max_length=200)  #组名
    book_name = models.CharField(max_length=200)  #书名
    target = models.CharField(max_length=200)    #目标
    operation = models.CharField(max_length=10)   #操作 已完成，未完成
    pay_type = models.CharField(max_length=10)    #已支付，未支付
    #create_time = models.DateTimeField(auto_now_add=True)  #更新时间
    #实际场景中，往往既希望在对象的创建时间默认被设置为当前值，又希望能在日后修改它.default=timezone.now来替换auto_now=True或auto_now_add=True
    update_time = models.DateTimeField('更新时间',auto_now=True) #更新时间
    create_time = models.DateTimeField('创建时间',default = timezone.now)  #创建时间(自动获取当前时间 )

    def __str__(self):   #__str__()方法告诉python如何将对象以str的方式显示出来。所以为每个模型类添加了__str__()方法
        return self.name
#读书表和用户表都会默认都会生成自增id，但在创建模型类时不需要创建该字段
class Guest(models.Model): #创建Guest用户类
#引用外键，及Event对象
    read_id = models.ForeignKey(Read, on_delete=models.CASCADE)  #关联读书计划表id,一条用户信息一定属于某一个读书计划，ForeignKey()来创建外键
    wd_num = models.CharField(max_length=8)  #工号
    name = models.CharField(max_length=64)  #姓名
    sex= models.CharField(max_length=10)    #性别
    phone = models.CharField(max_length=16)#手机号
    email = models.EmailField()#邮箱
    def __str__(self):
        return  self.name
    class Meta:
        unique_together = ("read_id", "phone")


