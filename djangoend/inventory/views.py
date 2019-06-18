from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json

API_PATH = 'http://tiered-backend:9125'

def list_inventory(request):
    book_list = requests.get('{}/books'.format(API_PATH)).json()

    settings.LOG.info(book_list)

    if book_list['response'] == 'error':
        return render(request, 'inventory/admin_inventory.html', {'error': 'No inventory list found'})

    bl = json.loads(book_list['books'])

    for b in bl:
        b['id'] = b['_id']['$oid']

    return render(request, 'inventory/admin_inventory.html', {'books': bl})

def add_book(request):
    if request.method == 'POST':
        form_data = request.POST.dict()

        book_type = form_data.get('book_type')
        genre = form_data.get('book_genre')
        name = form_data.get('book_name')
        description = form_data.get('book_description')
        price = form_data.get('book_price')
        condition = form_data.get('book_condition')
        in_stock = form_data.get('in_stock')

        payload = {
            'type': book_type,
            'genre': genre,
            'description': description, 
            'price': price,
            'in_stock': in_stock
        }
        if book_type == 'used':
            payload['condition'] = condition

        r = requests.put('{}/book/{}'.format(API_PATH, name), json=payload)
        settings.LOG.info(r.json())

        return redirect('list_inventory')

    return render(request, 'inventory/add_book.html')

def edit_book(request):
    if request.method == 'POST':
        form_data = request.POST.dict()

        book_name = form_data.get('old_book_name')
        book_type = form_data.get('book_type')
        genre = form_data.get('book_genre')
        name = form_data.get('book_name')
        description = form_data.get('book_description')
        price = form_data.get('book_price')
        condition = form_data.get('book_condition')
        in_stock = form_data.get('in_stock')

        payload = {
            'edit': True,
            'name': name,
            'type': book_type,
            'genre': genre,
            'description': description, 
            'price': price,
            'in_stock': in_stock
        }
        if book_type == 'used':
            payload['condition'] = condition

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=payload)
        settings.LOG.info(r.json())

        return redirect('list_inventory')

    book_name = request.GET.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    settings.LOG.info(book)

    return render(request, 'inventory/edit_book.html', {'book': json.loads(book['book'])})

def delete_book(request):
    book_name = request.GET.get('name')

    r = requests.delete('{}/book/{}'.format(API_PATH, book_name)).json()
    settings.LOG.info(r)

    return redirect('list_inventory')