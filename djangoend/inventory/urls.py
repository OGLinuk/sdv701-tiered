from django.urls import path
from . import views

urlpatterns = [
    path('list_inventory', views.list_inventory, name='list_inventory'),
    path('search_inventory', views.search_inventory, name='search_inventory'),
    path('add_book', views.add_book, name='add_book'),
    path('edit_book', views.edit_book, name='edit_book'),
    path('delete_book', views.delete_book, name='delete_book'),
]