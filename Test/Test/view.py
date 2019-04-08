from django.shortcuts import render

def hello(request):
    context={}
    context['hello']='hello'
    return render(request,'hello.html',context)