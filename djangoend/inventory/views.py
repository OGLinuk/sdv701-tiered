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

    book_list = json.loads(book_list['books'])

    for b in book_list:
        b['id'] = b['_id']['$oid']

    return render(request, 'inventory/admin_inventory.html', {'books': book_list})

def search_inventory(request):
    if request.method == 'POST':
        form_data = request.POST.dict()

        by_genre = form_data.get('search_by_genre')
        by_type = form_data.get('search_by_type')

        settings.LOG.info('{}\n{}'.format(by_genre, by_type))

        if by_genre != 'none':
            book_list = requests.get('{}/books_genre/{}'.format(API_PATH, by_genre)).json()
            settings.LOG.info(book_list)

            if book_list['response'] == 'error':
                return render(request, 'customer/customer.html', {'error': 'No inventory list found by genre'})

        if by_type != 'none':
            book_list = requests.get('{}/books_type/{}'.format(API_PATH, by_type)).json()
            settings.LOG.info(book_list)

            if book_list['response'] == 'error':
                return render('customer/customer.html', {'error': 'No inventory list found by type'})

        if by_genre == 'none' and by_type == 'none':
            return render(request, 'customer/customer.html', {'status': 'Please select search by option ...'})
        
        book_list = json.loads(book_list['books'])

        for b in book_list:
            b['id'] = b['_id']['$oid']  

        return render(request, 'inventory/customer_inventory.html', {'books': book_list})

    return render(request, 'inventory/customer_inventory.html')

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