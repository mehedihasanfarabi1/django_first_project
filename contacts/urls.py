from django.urls import path
from .views import contactPage

urlpatterns = [
    path('', contactPage, name='contact'),
]
