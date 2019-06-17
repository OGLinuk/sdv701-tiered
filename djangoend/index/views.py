from django.shortcuts import render

def index(request):
    return render(request, 'index/index.html')

def admin(request):
    return render(request, 'admin/admin.html')

def customer(request):
    return render(request, 'customer/customer.html')