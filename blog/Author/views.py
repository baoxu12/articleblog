from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from Author.models import *
import hashlib
from django.core.paginator import Paginator
# Create your views here.


# 装饰器
def LoginVaild(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        username_session = request.session.get("username")
        if username and username_session and username == username_session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Author/login/')
    return inner

## 密码加密
def setPassword(password):
    ## 实现一个密码加密
    md5 = hashlib.md5()  ## 创建一个md5的实例对象
    md5.update(password.encode())  ## 进行加密
    result = md5.hexdigest()
    return result

## 登录
def login(request):
    if request.method == "POST":
        error_msg=''
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = Author.objects.filter(email=email).first()
            if user:
                ## 用户存在
                if user.password == setPassword(password):
                    response = HttpResponseRedirect('/Author/index/1/')
                    response.set_cookie("username",user.username)
                    response.set_cookie("userid",user.id)
                    request.session['username'] = user.username
                    return response
                else:
                    error_msg = '密码错误'
            else:
                error_msg = '用户不存在'
        else:
            error_msg = '邮箱不可以为空'

    return render(request,'adm/login.html')

## 注册
def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        if email:
            #  判断邮箱是否存在
            loginUser = Author.objects.filter(email=email).first()
            if not loginUser:
                user = Author()
                user.email = email
                user.username = email
                user.password = setPassword(password)
                user.save()
                error_msg = "注册成功"
            else:
                error_msg = '邮箱已经被注册，请登录'
        else:
            error_msg = '邮箱不可以为空'

    return render(request,'adm/register.html',locals())


## 主页
@LoginVaild
def index(request,page=1):
    page = int(page)
    type1 = Type.objects.all()
    username = request.COOKIES.get("username")
    user = Author.objects.filter(username=username).first()

    key = request.GET.get("key")
    type = request.GET.get("req_type")
    if type == "search":
        article = Article.objects.filter(title__contains=key).all()
    else:
        article = Article.objects.order_by("-date")
    paginator = Paginator(article, 6)
    page_obj = paginator.page(page)
    current_page = page_obj.number  # 获取当前页码
    start = current_page - 3  # 使遍历的起始页面固定在当前页面前面第三个4---->1
    if start < 1:  # 在起始页面小于1时，变0
        start = 0
    end = current_page + 2  # 终止页面加2 如4 ----> 5
    if end > paginator.num_pages:  # 终止页面大于当前页面变为当前页面
        end = paginator.num_pages
    if start == 0:  # 起始页面为0,终止页面加5
        end = 5
    if end == paginator.num_pages:  # 终止页面为当前页面，起始页面加5
        start = paginator.num_pages - 5
    if end == paginator.num_pages - 1:  # 终止页面为当前页面前一个页面时起始页面减4
        start = paginator.num_pages - 4

    page_range = paginator.page_range[start:end]

    recommend_article = Article.objects.filter(recommend=1).all()[:7]
    click_article = Article.objects.order_by("-click")[:12]

    return render(request,'adm/index.html',locals())

# 登出
def logout(request):
    response = HttpResponseRedirect("/Author/login/")
    # 删除cookie
    keys = request.COOKIES.keys()
    for one in keys:

        response.delete_cookie(one)
    # 删除session 删除指定session 删除的是保存在服务器上面的值
    del request.session["username"]

    return response

## 模板
@LoginVaild
def base(request):
    username = request.COOKIES.get("username")
    user = Author.objects.filter(username=username).first()

    return render(request,'adm/base.html',locals())

## 文章详情
@LoginVaild
def articledetails(request,id):
    user_id = request.COOKIES.get("userid")
    user = Author.objects.get(id=user_id)
    type1 = Type.objects.all()
    id = int(id)
    article = Article.objects.get(id=id)

    return render(request,'adm/articledetails.html',locals())

## 类别
@LoginVaild
def  type(request,type,page=1):
    type1 = Type.objects.all()
    page = int(page)
    article = Type.objects.get(name=type).article_set.order_by('-date')
    # 分页
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)   # 通过上面的代码再倒数第二页，第一页和最后一页会出现显示在页面上的固定页数不足的情况，要通过以下代码来调整
    # 获取当前页
    current_page = page_obj.number # 获取当前页码
    start = current_page -3  # 使遍历的起始页面固定在当前页面前面第三个4---->1
    if start < 1:  # 在起始页面小于1时，变0
        start = 0
    end = current_page +2  # 终止页面加2 如4 ----> 5
    if end > paginator.num_pages:  # 终止页面大于当前页面变为当前页面
        end = paginator.num_pages
    if start == 0:   # 起始页面为0,终止页面加5
        end = 5
    if end == paginator.num_pages:  # 终止页面为当前页面，起始页面加5
        start = paginator.num_pages - 5
    if end == paginator.num_pages - 1: # 终止页面为当前页面前一个页面时起始页面减4
        start = paginator.num_pages - 4

    page_range = paginator.page_range[start:end]  # range后面的括号里面是下标
    return render(request, 'adm/type.html', locals())

## 写博客

def writeblog(request):
    type = Type.objects.all()

    username = request.COOKIES.get("username")
    user = Author.objects.filter(username=username).first()
    if request.method == "POST":
        ## 获取数据,保存数据

        data = request.POST
        article = Article()
        type_id= data.get("type")
        author_name = data.get("author")
        ## 多对多关系
        article.title = data.get('title')
        article.date = data.get('date')
        article.content = data.get('content')
        article.description = data.get('description')
        article.recommend = data.get('recommend')
        article.click = data.get('click')
        article.picture = request.FILES.get('picture')
        article.save()
        ## 一对多关系 添加类别
        article.type = Type.objects.get(id = type_id)

        user_id = request.COOKIES.get("userid")
        ## 一对多关系添加
        article.author = Author.objects.get(id=user_id)

        article.save()

    return render(request,'adm/writeblog.html',locals())

## 个人信息页
@LoginVaild
def personal_info(request):
    user_id = request.COOKIES.get("userid")
    user = Author.objects.get(id=user_id)

    if request.method == "POST":
        ## 获取数据,保存数据
        data = request.POST
        user.username = data.get('username')
        user.phone_number = data.get('phone_number')
        user.age = data.get('age')
        user.gender = data.get('gender')
        user.address = data.get('address')
        user.photo = request.FILES.get('photo')
        user.save()

    return render(request,'adm/personal_info.html',locals())

@LoginVaild
def myblog(request,page=1):
    type1 = Type.objects.all()
    page = int(page)
    username = request.COOKIES.get("username")
    user = Author.objects.filter(username=username).first()
    author = Author.objects.filter(username=username).first()

    article_id = request.GET.get("article_id")
    Article.objects.filter(id=article_id).delete()


    article = Article.objects.filter(author_id = author.id).all().order_by("-date")
    paginator = Paginator(article, 6)
    page_obj = paginator.page(page)
    current_page = page_obj.number  # 获取当前页码
    start = current_page - 3  # 使遍历的起始页面固定在当前页面前面第三个4---->1
    if start < 1:  # 在起始页面小于1时，变0
        start = 0
    end = current_page + 2  # 终止页面加2 如4 ----> 5
    if end > paginator.num_pages:  # 终止页面大于当前页面变为当前页面
        end = paginator.num_pages
    if start == 0:  # 起始页面为0,终止页面加5
        end = 5
    if end == paginator.num_pages:  # 终止页面为当前页面，起始页面加5
        start = paginator.num_pages - 5
    if end == paginator.num_pages - 1:  # 终止页面为当前页面前一个页面时起始页面减4
        start = paginator.num_pages - 4

    page_range = paginator.page_range[start:end]

    # recommend_article = Article.objects.filter(recommend=1).all()[:7]
    # click_article = Article.objects.order_by("-click")[:12]

    return render(request,'adm/myblog.html',locals())

def alter(request,id):
    id = int(id)
    type = Type.objects.all()
    user_id = request.COOKIES.get("userid")
    user = Author.objects.get(id=user_id)
    article = Article.objects.filter(id = id).first()


    if request.method == "POST":
        ## 获取数据,保存数据
        data = request.POST
        type_id = data.get("type")
        article.title = data.get('title')
        article.content = data.get('content')
        article.description = data.get('description')
        article.recommend = data.get('recommend')
        article.click = data.get('click')
        article.date = data.get('date')
        article.picture = request.FILES.get('picture')
        article.save()
        article.type = Type.objects.get(id = type_id)
        article.save()

    return render(request,'adm/alter.html',locals())
