from django.contrib import admin
from django.contrib import admin
from .models import Category,Product,Sale,DetSale,Client

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(DetSale)
admin.site.register(Client)