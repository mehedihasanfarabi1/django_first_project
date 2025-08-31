from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from .form import usersForm
from services.models import Service
from news.models import News
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail


def send_test_mail(request):
    subject = "Welcome to the new site from Mehedi Hasan"
    from_email = "softwaredevelopers400@gmail.com"
    recipient_list = ["rrokon304@gmail.com","mehedihasanfarabi10@gmail.com"]

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to MySite</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 40px auto;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background-color: #1877f2;
                color: #fff;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
            }
            .content {
                padding: 30px;
                color: #333;
                text-align: center;
                font-size: 16px;
                line-height: 1.6;
            }
            .btn {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                color: #fff;
                background-color: #1877f2;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }
            .footer {
                background-color: #f0f2f5;
                padding: 15px;
                text-align: center;
                font-size: 14px;
                color: #777;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                MySite
            </div>
            <div class="content">
                <h2>Welcome to MySite!</h2>
                <p>Thanks for joining us. Click the button below to visit our homepage.</p>
                <a href="http://127.0.0.1:8000" class="btn">Visit Homepage</a>
            </div>
            <div class="footer">
                &copy; 2025 MySite. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, "", from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse("✅ Email Sent!")



def homePage(request):
    newsData = News.objects.all()

    # Search functionality
    search_str = request.GET.get('searchBox')
    if search_str:
        serviceData = Service.objects.filter(service_title__icontains=search_str)
    else:
        serviceData = Service.objects.all()

    # Pagination
    paginator = Paginator(serviceData, 1)  # 3 items per page
    page_number = request.GET.get('page')
    finalServicePaginatorData = paginator.get_page(page_number)

    # Pre-calculate variables for template
    current = finalServicePaginatorData.number
    prev_page = current - 1
    next_page = current + 1
    total_pages = paginator.num_pages

    context = {
        'serviceData': finalServicePaginatorData,
        'newsData': newsData,
        'search_str': search_str,
        'current': current,
        'prev_page': prev_page,
        'next_page': next_page,
        'total_pages': total_pages
    }
    return render(request, 'index.html', context)

# def homePage(request):
#     newsData = News.objects.all()
#     # serviceData = Service.objects.all().order_by('-service_title')[:2]
#      # for i in serviceData:
#     #     print(i.service_icon)
#     search_str = request.GET.get('searchBox')
    
#     if search_str:
#         serviceData = Service.objects.filter(service_title__icontains=search_str)
#     else:
#         serviceData = Service.objects.all()
    
#     # Pagination
#     paginator = Paginator(serviceData, 1)  # 3 per page
#     page_number = request.GET.get('page')
#     finalServicePaginatorData = paginator.get_page(page_number)

#     data = {
#         'serviceData': finalServicePaginatorData,
#         'newsData': newsData,
#         'search_str': search_str  # Optional: to keep search input value
#     }
#     return render(request,'index.html',data)


def aboutUs(request):
    return render(request,'about-us.html')

def newsDetails(request, slug):
    newsData = News.objects.get(news_slug=slug)
    
    data = {
        'slug': slug,
        'newsData': newsData
    }
    return render(request, 'newsDetail.html', data)


def calculator(request):
    result = None
    if request.method == 'POST':
        num1 = eval(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operator = request.POST.get('operator')

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error! Division by zero."

    return render(request, 'calculator.html', {'result': result})

def evenodd(request):
    result = None
    if request.method == 'POST':
        if request.POST.get('number')=="":
             return render(request, 'evenodd.html', {'error': True}) 
        try:
            num = int(request.POST.get('number'))
            if num % 2 == 0:
                result = f"{num} is Even ✅"
            else:
                result = f"{num} is Odd 🔥"
        except:
            result = "Please enter a valid number."
    return render(request, 'evenodd.html', {'result': result}) 



def marksheet(request):
    total = percentage = grade = None
    fail_count = 0
    marks = {}

    if request.method == 'POST':
        try:
            # Subject-wise marks collect করা
            bangla = float(request.POST.get('bangla', 0))
            english = float(request.POST.get('english', 0))
            math = float(request.POST.get('math', 0))
            science = float(request.POST.get('science', 0))
            social = float(request.POST.get('social', 0))
            ict = float(request.POST.get('ict', 0))

            marks = {
                'Bangla': bangla,
                'English': english,
                'Math': math,
                'Science': science,
                'Social': social,
                'ICT': ict
            }

            # Fail count check
            for sub, mark in marks.items():
                if mark < 40:
                    fail_count += 1

            # Total & Percentage
            total = sum(marks.values())
            percentage = (total / 600) * 100  # 6 subjects, each 100 marks

            # Grade calculation
            if fail_count > 0:
                grade = "Fail ❌"
            elif percentage >= 80:
                grade = "A+ 🎉"
            elif percentage >= 70:
                grade = "A"
            elif percentage >= 60:
                grade = "A-"
            elif percentage >= 50:
                grade = "B"
            elif percentage >= 40:
                grade = "C"
            else:
                grade = "Fail ❌"

        except:
            grade = "⚠️ Please enter valid numbers."

    return render(request, 'marksheet.html', {
        'marks': marks,
        'total': total,
        'percentage': percentage,
        'grade': grade,
        'fail_count': fail_count
    })

def serviceUs(request):
    if request.method == "GET":
        outputName = request.GET.get('name')
    return render(request,'services.html',outputName)


def contactUs(request):
    return render(request,'contact.html')
# def form(request):
#     try:
#         # name = request.GET['fullname']
#         # email = request.GET['email']
#         # phone = request.GET['phone']
#         # address = request.GET['address']
        
#         # print('Name = '+ name +"Email = " + email+'<br>')
#         # print('Phone = '+phone+ "Address = "+address)
#         data= {}
#         if request.method == 'POST':
#             name = request.POST['fullname']
#             email = request.POST['email']
#             phone = request.POST['phone']
#             address = request.POST['address']
            
#             data = {
#                 'name' : name,
#                 'email' : email
#             }
            
#             # url = "/services/?name={}".format(name)
            
#             return HttpResponseRedirect('/services')
#             # return redirect(url)
#             # return HttpResponseRedirect(url)
#     except:
#         pass
#     return render(request,'forms.html',data)


def form(request):
    try:
        fn = usersForm()
        data= {'form':fn}
        if request.method == 'POST':
            name = request.POST['fullname']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            
            data = {
                'form' : fn,
                
            }
            
            # url = "/services/?name={}".format(name)
            
            return HttpResponseRedirect('/services')
            # return redirect(url)
            # return HttpResponseRedirect(url)
    except:
        pass
    return render(request,'forms.html',data)

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