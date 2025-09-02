from django.urls import path
from .views import create_product, product_list,edit_product,delete_product,product_details

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/create/',create_product, name='create_product'),
    path('products/view/<int:id>/',product_details, name='product_details'),
    path('products/edit/<int:id>/',edit_product, name='edit_product'),
    path('products/delete/<int:id>/',delete_product, name='delete_product'),

]
