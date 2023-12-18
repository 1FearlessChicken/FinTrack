from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="inventory"),
    path('add-inventoryItem/', views.add_inventory, name="add-inventoryItem"),
    path('edit-inventoryItem/<int:id>', views.inventory_edit, name="inventoryItem-edit"),
    path('inventoryItem-delete/<int:id>', views.delete_inventory, name="inventoryItem-delete"),
    path('search-inventoryItem/', csrf_exempt(views.search_inventory), name="search-inventoryItem"),
    
    
] 