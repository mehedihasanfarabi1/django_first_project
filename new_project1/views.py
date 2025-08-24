from django.http import HttpResponse
from django.shortcuts import render

def homePage(request):
    return render(request,'index.html')
def aboutUs(request):
    return render(request,'about-us.html')
def serviceUs(request):
    return render(request,'services.html')
def contactUs(request):
    return render(request,'contact.html')

def homePage2(request):

    # data = {
    #     'title' : 'Home Page',
    #     'datas' : 'Welcome to the new home page',
    #     'list': ['PHP','JAVA','C++','JAVASCRIPT'],
    #     'numbers': [10,20,30,40,50,60],
    #     'student_details' : [{
    #         'name' : "Mehedi Hasan",
    #         'age' : 21,
    #                         },
    #                         {
    #         'name' : "Robiul Hasan",
    #         'age' : 23,
    #                         }]
    # }
    return render(request,'index2.html')

def about(request):
    return HttpResponse('Welcome to the new world')

def dynamicRoute(request,newid):
    return HttpResponse(newid)

def dynamicRoute1(request,newids):
    return HttpResponse(newids)