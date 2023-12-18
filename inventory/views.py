from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference


# @login_required(login_url='/authentication/login')
@login_required(login_url="/authentication/login")
def index(request):
    location = Location.objects.all()
    inventoryItems = Inventory_item.objects.filter(owner=request.user)
    paginator = Paginator(inventoryItems, 10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'inventoryItems' : inventoryItems,
        'page_obj' : page_obj,        
    }
    return render(request, 'inventory/index.html', context)


def add_inventory(request):
    locations = Location.objects.all()
    context = {
            'locations' : locations,
            'values' : request.POST,
        }
    if request.method == "GET":
        return render(request, 'inventory/add_inventory.html', context)

    if request.method == 'POST':
        quantity = request.POST['quantity']
        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'inventory/add_inventory.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'inventory/add_inventory.html', context)

        date = request.POST['entry_date']
        location = request.POST['location']
        
        Inventory_item.objects.create(owner=request.user, quantity=quantity, date=date, location=location, description=description)
        messages.success(request, 'Item saved successfully')
        
        return redirect('inventory')
    
def inventory_edit(request, id):
    inventoryItem = Inventory_item.objects.get(pk=id)
    locations = Location.objects.all()
    context = {
        'inventoryItem' : inventoryItem,
        'values' : inventoryItem,
        'locations' : locations,
    }
    
    if request.method == "GET":
        return render(request, 'inventory/edit_inventory.html', context)
    
    if request.method == "POST":
        quantity = request.POST['quantity']
        date = request.POST['inventoryItem_date']
        location = request.POST['location']
        description = request.POST['description']
        
        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'inventory/edit_inventory.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'inventory/edit_inventory.html', context)
        
        inventoryItem.owner=request.user
        inventoryItem.quantity=quantity
        inventoryItem.date=date
        inventoryItem.location=location
        inventoryItem.description=description
        
        inventoryItem.save()
        messages.success(request, 'Inventory updated successfully')
        
        return redirect('inventory')
    
def delete_inventory(request, id):
    inventoryItem = Inventory_item.objects.get(pk=id)
    inventoryItem.delete()
    
    messages.success(request, "Item Removed")
    return redirect('inventory')



def search_inventory(request):
    if request.method == "POST":
        
        search_str = json.loads(request.body).get('searchText')
        
        inventoryItems = Inventory_item.objects.filter(
            quantity__istartswith=search_str, owner=request.user) | Inventory_item.objects.filter(
                date__istartswith=search_str, owner=request.user) | Inventory_item.objects.filter(
                    description__icontains=search_str, owner=request.user) | Inventory_item.objects.filter(
                        location__icontains=search_str, owner=request.user)
      
        data = inventoryItems.values()
        
        return JsonResponse(list(data), safe=False)