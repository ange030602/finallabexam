# admin.py

from django.contrib import admin
from .models import UserProfile, Product, Checkout

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Checkout)
