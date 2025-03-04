from django.contrib import admin
from .models import Item, Order, Tax, Discount

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'price', 'currency']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['items', 'tax', 'discount']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    search_fields = ['name']

