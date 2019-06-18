from django.shortcuts import render
from django.conf import settings
import requests
import json

API_PATH = 'http://tiered-backend:9125'

def list_inventory(request):
    book_list = requests.get('{}/books'.format(API_PATH)).json()

    settings.LOG.info(book_list)

    if book_list['response'] == 'error':
        return render(request, 'inventory/admin_inventory.html', error='No inventory list found')

    bl = json.loads(book_list['books'])

    for b in bl:
        b['id'] = b['_id']['$oid']

    return render(request, 'inventory/admin_inventory.html', {'books': bl})