from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json

API_PATH = 'http://tiered-backend:9125'

def list_orders(request):
    order_list = requests.get('{}/orders'.format(API_PATH)).json()
    settings.LOG.info(order_list)

    if order_list['response'] == 'error':
        return render(request, 'admin/admin.html', {'error': 'No order list found'})
        
    order_list = json.loads(order_list['orders'])

    for o in order_list:
        o['id'] = o['_id']['$oid']  
        
    return render(request, 'orders/orders.html', {'orders': order_list})

def order_book(request):
    if request.method == 'POST':
        form_data = request.POST.dict()

        order_quantity = form_data.get('quantity')
        book_name = form_data.get('name')
        customer_name = form_data.get('customer_name')
        customer_address = form_data.get('customer_address')

        book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
        book = json.loads(book['book'])

        book['in_stock'] -= int(order_quantity)

        book_payload = {
            'edit': True,
            'name': book['name'],
            'type': book['type'],
            'genre': book['genre'],
            'description': book['description'], 
            'price': book['price'],
            'in_stock': book['in_stock']
        }
        if book['type'] == 'used':
            book_payload['condition'] = book['condition']

        r = requests.put('{}/book/{}'.format(API_PATH, book_name), json=book_payload)
        settings.LOG.info(r.json())

        order_payload = {
            'book_id': book['_id']['$oid'],
            'order_quantity': order_quantity,
            'customer_name': customer_name,
            'customer_address': customer_address
        }

        r = requests.put('{}/order/{}'.format(API_PATH, book_name), json=order_payload)
        settings.LOG.info(r.json())

        return render(request, 'customer/customer.html', {'status': 'Order placed successfully ...'})

    book_name = request.GET.get('name')
    book = requests.get('{}/book/{}'.format(API_PATH, book_name)).json()
    settings.LOG.info(book)

    return render(request, 'orders/place_order.html', {'book': json.loads(book['book'])})

def delete_order(request):
    order_id = request.GET.get('oid')
    book_id = request.GET.get('bid')
    book_name = request.GET.get('bname')

    payload = {
        'order_id': order_id,
        'book_id': book_id
    }

    r = requests.delete('{}/order/{}'.format(API_PATH, book_name), json=payload).json()
    settings.LOG.info(r)

    return redirect('list_orders')