from django.urls import path
from . import views

urlpatterns = [
    path('list_orders', views.list_orders, name='list_orders'),
    path('order_book', views.order_book, name='order_book'),
    path('delete_order', views.delete_order, name='delete_order'),
]