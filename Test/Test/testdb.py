# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from TestModel.models import Test
from django.shortcuts import render
 
# 数据库操作
def testdb(request):
    list = Test.objects.all()
    return render(request,'电影top.html',{'list':list})
def index(request):
    return render(request,'index.html',locals())