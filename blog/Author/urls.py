from django.urls import path,re_path
from Author.views import *

urlpatterns = [
    path("login/",login),
    path("register/",register),
    re_path('index/(?P<page>\d+)', index),
    path("logout/",logout),
    path("base/",base),
    path("writeblog/",writeblog),
    re_path("myblog/(?P<page>\d+)",myblog),
    path("personal_info/",personal_info),
    re_path("alter/(?P<id>\d+)",alter),
    re_path("articledetails/(?P<id>\d+)",articledetails),
    re_path('type/(?P<type>\w+)/(?P<page>\d+)', type),
]