from django import forms 
from .models import Transection
from accounts.models import UserBankAccount,User
from .constants import TRANSFER_MONEY
class TransectionForm(forms.ModelForm):
    class Meta:
        model=Transection
        fields=['amount','transection_type']
    def __init__(self,*args,**kwargs):
            self.user_account = kwargs.pop('account')
            super().__init__(*args,**kwargs)
            self.fields['transection_type'].disabled=True #ei field disable thakbe
            self.fields['transection_type'].widget=forms.HiddenInput #ay field hidden thakbe
    def save(self,commit=True):
            self.instance.account=self.user_account
            self.instance.balance_after_transection=self.user_account.balance
            return super().save()


class DepositeForm(TransectionForm):
    def clean_amount(self):
        min_diposite_amount=100
        amount=self.cleaned_data.get('amount')
        if amount < min_diposite_amount:
            raise forms.ValidationError(
                f'you need to deposite minimum {min_diposite_amount} $'
            )
        return amount
class WithdrawForm(TransectionForm):
    def clean_amount(self):
        account=self.user_account
        min_withdraw=500
        max_withdraw=200000
        balance=account.balance
        amount=self.cleaned_data.get('amount')
        if amount<min_withdraw:
            raise forms.ValidationError(
                f'you need to withdraw at least {min_withdraw} $'
            )
        if amount > max_withdraw:
            raise forms.ValidationError(
                f"you can't withdraw up to {max_withdraw} $"
            )
        if amount > balance:
            raise forms.ValidationError(
                f"you don't have enough balance in your account"
            )
        return amount

class LoanForm(TransectionForm):
    def clean_amount(self):
        return self.cleaned_data.get('amount')
class TransferMoneyForm(forms.ModelForm):
     accountNo=forms.IntegerField()
     class Meta:
          model=Transection
          fields=['accountNo','amount']
     def __init__(self,*args,**kwargs):
          self.user_account=kwargs.pop('account')
          super().__init__(*args,**kwargs)
     def save(self,commit=True):
            self.instance.account=self.user_account
            self.instance.transection_type=TRANSFER_MONEY;
            self.instance.balance_after_transection=self.user_account.balance
            return super().save()
     def clean_amount(self):
          amount=self.cleaned_data.get('amount')
          account=self.user_account
          if account.balance<amount:
               raise forms.ValidationError(f"Your Account balance is Low")
          return amount
     def clean_accountNo(self):
        # print('hello vai')
        account_no = self.cleaned_data.get('accountNo')
        
        try:
            print('hello vaiya')
            receiver_account = UserBankAccount.objects.get(account_no=account_no)
            print('hello vaiya')
            
        except UserBankAccount.DoesNotExist:
            print('hello vaiya dukse ami')
            raise forms.ValidationError('Invalid receiver account number.')
        return account_no
               

          
               
               
          

