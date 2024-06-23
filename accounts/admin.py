from django.contrib import admin

# Register your models here.
from .models import UserBankAccount,UserAddress
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)
