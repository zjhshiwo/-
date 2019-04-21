# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from TestModel.models import Test
from django.shortcuts import render
 
# 数据库操作
def testdb(request):
    return render(request,'首页.html')