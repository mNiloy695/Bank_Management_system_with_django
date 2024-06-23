from django.contrib import admin
from .models import Transection
from .views import send_mail
# Register your models here.
@admin.register(Transection)
class TransectionAdmin(admin.ModelAdmin):
    list_display=['account','amount','balance_after_transection','loan_approve']
    def save_model(self,request,obj,form,change):
        if obj.loan_approve==True:
            obj.account.balance+=obj.amount
            obj.balance_after_transection=obj.account.balance
            obj.account.save()
            send_mail(obj.account.user,obj.amount,'LOAN APPROVED','LOAN APPROVED')
        return super().save_model(request,obj,form,change)
