# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from TestModel.models import Test,phone
from django.shortcuts import render
 
# 数据库操作
def testdb(request):
    list = Test.objects.all()
    return render(request,'电影top.html',{'list':list})
def index(request):
    return render(request,'index.html',locals())
def jd(request):
    list = phone.objects.all()
    return render(request,'jd.html',{'list':list})