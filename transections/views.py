from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
# Create your views here.
from .forms import TransectionForm,DepositeForm,WithdrawForm,LoanForm,TransferMoneyForm
from django.views.generic import CreateView,ListView,View
from .models import Transection
from django.contrib.auth.mixins import LoginRequiredMixin
from .constants import DEPOSITE,WITHDRAW,LOAN,LOAN_PAID,TRANSFER_MONEY
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from accounts.models import User,UserBankAccount
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string

def send_mail(user,amount,subject,type):
        mail_subject=subject
        message=render_to_string('transections/mail.html',{
            'user':user,
            'type':type,
            'amount':amount
             
        })
        user_mail=user.email
        mail=EmailMultiAlternatives(mail_subject,'',to=[user_mail])
        mail.attach_alternative(message,'text/html')
        mail.send()
        
class TransectionCreateMinix(LoginRequiredMixin,CreateView):
    template_name='transections/transection_form.html'
    model=Transection
    title=''
    success_url=reverse_lazy('transaction_report')
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update(
            {
                'account':self.request.user.account
            }
        )
        return kwargs
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update(
            {
                'title':self.title
            }
        )
        return context
    
class DepositeMoneyView(TransectionCreateMinix):
    form_class=DepositeForm
    title='DEPOSITE'
    def get_initial(self):
        initial={'transection_type':DEPOSITE}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # transection_instance=form.save(commit=False)
        # transection_instance.amount=amount
        # transection_instance.save(
        #     update_fields=[
        #         'amount'
        #     ]
        # )
        print(account.balance)
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )
        print(f"New balance after deposit: {account.balance}")  # Check the updated balance
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        mail_subject='Deposite Money'
        message=render_to_string('transections/mail.html',{
            'user':self.request.user,
            'type':'Deposit',
            'amount':amount
             
        })
        user_mail=self.request.user.email
        mail=EmailMultiAlternatives(mail_subject,'',to=[user_mail])
        mail.attach_alternative(message,'text/html')
        mail.send()
        return super().form_valid(form)
    
class WithdrawMoneyView(TransectionCreateMinix):
    form_class=WithdrawForm
    title='Withdraw'
    def get_initial(self):
        initial={'transection_type':WITHDRAW}
        return initial
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount} $ withdraw successed !")
        mail_subject='Withdraw Money'
        message=render_to_string('transections/mail.html',{
            'user':self.request.user,
            'type':'Withdraw',
            'amount':amount
             
        })
        user_mail=self.request.user.email
        mail=EmailMultiAlternatives(mail_subject,'',to=[user_mail])
        mail.attach_alternative(message,'text/html')
        mail.send()
        return super().form_valid(form)
class LoanRequestView(TransectionCreateMinix):
    form_class=LoanForm
    title='LOAN'
    def get_initial(self):
        initial={'transection_type':LOAN}
        return initial
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=Transection.objects.filter(account=self.request.user.account,transection_type=LOAN,loan_approve=True).count()
        if current_loan_count>=3:
            return HttpResponse('you crossed the loan limitaion')
        messages.success(self.request,f'your {amount}$ loan request send succesfully')
        mail_subject='Loan Request'
        message=render_to_string('transections/mail.html',{
            'user':self.request.user,
            'type':'Loan Request',
            'amount':amount
             
        })
        user_mail=self.request.user.email
        mail=EmailMultiAlternatives(mail_subject,'',to=[user_mail])
        mail.attach_alternative(message,'text/html')
        mail.send()
        return super().form_valid(form)

class TransectionReportView(LoginRequiredMixin,ListView):
    template_name='transections/transaction_report.html'
    model=Transection
    balance=0
    def get_queryset(self):
        queryset=super().get_queryset().filter(account=self.request.user.account)
        start_date_str=self.request.GET.get('start_date')
        end_date_str=self.request.GET.get('end_date')
        if start_date_str and end_date_str:
             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
             queryset=queryset.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date)
             self.balance=Transection.objects.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance=self.request.user.account.balance
        return queryset.distinct()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context

class PayLoanView(LoginRequiredMixin,View):
    def get(self,request,loan_id):
        loan=get_object_or_404(Transection,id=loan_id)
        if loan.loan_approve:
           user_account=loan.account
           if user_account.balance > loan.amount:
               user_account.balance-=loan.amount
               loan.balance_after_transection=user_account.balance
               user_account.save()
               loan.transection_type=LOAN_PAID
               loan.save()
               return redirect('transaction_report')
           else:
               messages.error(self.request,f'your balance is low')
               return redirect('transection_report')
class LoanListView(LoginRequiredMixin,ListView):
    template_name='transections/loans_request.html'
    model=Transection
    context_object_name='loans'
    def get_queryset(self):
        queryset=Transection.objects.filter(account=self.request.user.account,transection_type=LOAN)
        return queryset

               
class TransferMoneyView(TransectionCreateMinix):
    form_class=TransferMoneyForm
    title='Transfer_Money'
    # def get_initial(self):
    #     initial={'transection_type':TRANSFER_MONEY}
    #     return initial
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        reciver_account_no=form.cleaned_data.get('accountNo')
        sender_account=self.request.user.account
        reciver_bank_account=UserBankAccount.objects.get(account_no=reciver_account_no)
        # reciver=User.objects.get(account=reciver_bank_account)
        reciver_bank_account.balance +=amount
        sender_account.balance -=amount
        reciver_bank_account.save(update_fields=['balance'])
        sender_account.save(update_fields=['balance'])
        messages.success(self.request,f'You send {amount}$ to { reciver_account_no} sucessfully')
        send_mail(self.request.user,amount,'Transfer Money','Transfer Money')
        # print(reciver_bank_account.user.email)
        send_mail(reciver_bank_account.user,amount,'Recive Money','Recive Money')
        return super().form_valid(form)




# class CustomLoginView(auth_views.LoginView):
    