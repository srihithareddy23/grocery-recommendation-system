from django.contrib import admin
from .models import grocery_store
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
from .models import grocery_store
from import_export.admin import ImportExportModelAdmin

admin.site.register(
    [Admin, Customer, Category, Product, Cart, CartProduct, Order, ProductImage])

@admin.register(grocery_store)
class userdat(ImportExportModelAdmin):
    pass

@admin.register(history)
class userdat(ImportExportModelAdmin):
    pass