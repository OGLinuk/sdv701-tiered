from django.urls import path
from . import views

urlpatterns = [
    path('list_orders', views.list_orders, name='list_orders')
]