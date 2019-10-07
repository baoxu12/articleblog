from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

## 作者
class Author(models.Model):
    email = models.EmailField(verbose_name='邮箱')
    password = models.CharField(max_length=32,verbose_name='密码')
    username = models.CharField(max_length=32,null=True,blank=True,verbose_name='用户名')
    ## null 针对数据库，可以为空
    ## blank针对表单，表示在表单中该字段可以不填，对数据库没有影响
    phone_number = models.CharField(max_length=11,null=True,blank=True,verbose_name='手机号')
    photo = models.ImageField(upload_to='images',null=True,blank=True,verbose_name='图像')
    age = models.IntegerField(null=True,blank=True,verbose_name='年龄')
    gender = models.CharField(max_length=4,null=True,blank=True,verbose_name='性别')
    address = models.TextField(null=True,blank=True,verbose_name='地址')
    def __str__(self):
        return self.username
    class Meta:
        db_table='Author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

class Type(models.Model):
    name = models.CharField(max_length=32,verbose_name='类型名')
    description = models.TextField(verbose_name='类型描述')
    def __str__(self):
        return self.name

    class Meta:
        db_table='type'
        verbose_name = '类型'
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='文章名')
    date = models.DateField(auto_now=True,verbose_name='日期')
    # content = models.TextField(verbose_name='文章内容')
    content = RichTextField(verbose_name='文章内容')
    # description = models.TextField(verbose_name='文章描述')
    description = RichTextField(verbose_name='文章描述')
    ## 图片类型
    ## upload_to 指定文件上传位置 static目录下的images目录中
    picture = models.ImageField(upload_to='images',verbose_name='图片')
    # 推荐
    recommend = models.IntegerField(verbose_name='推荐',default=0) ## 0代表不推荐 1代表推荐
    # 点击率
    click = models.IntegerField(verbose_name='点击率',default=0)

    author = models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1,verbose_name='作者')
    type = models.ForeignKey(to=Type,on_delete=models.CASCADE,default=1,verbose_name='类别')

    def __str__(self):
        return self.title
    class Meta:
        db_table='article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name