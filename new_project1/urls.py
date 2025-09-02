
from django.contrib import admin
from django.urls import path,include
from new_project1 import views
from django.conf import settings
from django.conf.urls.static import static
from .views import send_test_mail

urlpatterns = [
    path('',views.homePage),
    path('home2/',views.homePage2),
    path('admin/', admin.site.urls),
    path('about',views.about),
    path('about-us',views.aboutUs,name="newabout"),
    path('services',views.serviceUs),
    path('contact',views.contactUs),
    path('form',views.form),
    path('calculator/',views.calculator),
    path('evenodd/',views.evenodd),
    path('marksheet/',views.marksheet),
    path('news_details/<slug>/', views.newsDetails, name="news_details"),
    path('dynamic-route/<str:newid>',views.dynamicRoute),
    path('dynamic-route/<newids>',views.dynamicRoute1),
    path('contact/', include('contacts.urls')),
    path('sendmail/', send_test_mail),
    path('', include('products.urls')),
    path('', include('billing.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


