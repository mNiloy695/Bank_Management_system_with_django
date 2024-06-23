from django.db import models
from accounts.models import UserBankAccount
# Create your models here.
from .constants import  TRSANSECTION_TYPE
class Transection(models.Model):
    account=models.ForeignKey(UserBankAccount,on_delete=models.CASCADE,related_name='transection')
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    balance_after_transection=models.DecimalField(max_digits=12,decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)
    transection_type=models.IntegerField(choices= TRSANSECTION_TYPE)
    loan_approve=models.BooleanField(default=False)
    # account_no=models.IntegerField()
    class Meta:
        ordering=['timestamp']
