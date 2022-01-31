from tkinter import E
from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

#Create yout views here.

def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_items':0,'get_cart_total':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products,'cartItems':cartItems }
	return render(request, 'store/store.html', context)

def cart(request):
	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_items':0,'get_cart_total':0}
		cartItems = order['get_cart_items']

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_items':0,'get_cart_total':0}
		cartItems = order['get_cart_items']
		
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body) #need to import json
	productId = data['productId'] #dictionary and naming is from fetch body of cart.js
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, create = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = ( orderItem.quantity +1 )
	elif action == 'remove':
		orderItem.quantity = ( orderItem.quantity -1 )
	
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)