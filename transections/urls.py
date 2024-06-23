from django.urls import path
from .views import LoanListView,PayLoanView,DepositeMoneyView,TransectionReportView,WithdrawMoneyView,LoanRequestView,TransferMoneyView

urlpatterns = [
    path("deposit/", DepositeMoneyView.as_view(), name="deposit_money"),
    path("report/", TransectionReportView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("loan_request/", LoanRequestView.as_view(), name="loan_request"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
    path("loans/<int:loan_id>/", PayLoanView.as_view(), name="pay"),
    path("transfer_money/",TransferMoneyView.as_view(), name="transfer_money"),
]