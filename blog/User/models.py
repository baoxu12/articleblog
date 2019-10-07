from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(verbose_name='邮箱',default=0)
    password = models.CharField(max_length=32, verbose_name='密码')
    username = models.CharField(max_length=32, null=True, blank=True, verbose_name='用户名')
    ## null 针对数据库，可以为空
    ## blank针对表单，表示在表单中该字段可以不填，对数据库没有影响
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='图像')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
    gender = models.CharField(max_length=4, null=True, blank=True, verbose_name='性别')
    address = models.TextField(null=True, blank=True, verbose_name='地址')

    class Meta:
        db_table='user'