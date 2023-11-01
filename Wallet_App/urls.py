from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'Wallet_App'

urlpatterns = [
     path('',views.wallet,name='wallet_page'),
     path('deposit-checkout/',views.deposit_checkout, name='deposit_checkout'),
     path('confirm-deposit/', views.confirm_deposit, name = 'confirm_deposit'),
     path('status/', views.deposit_complete, name='deposit_complete'),
     path('deposit-transaction/<val_id>/<tran_id>/<payment_type>',views.deposit_transaction, name='deposit_transaction'),
     path('payemnt-checkout/<order_id>/', views.order_checkouts, name='payment_checkout'),
     path('unsuccess-checkouts/', views.unsuccess_checkouts, name='unsuccess_checkouts'),
     path('payment-confirm/<order_id>', views.payment_confirm, name='confirm_payment'),
     path('complete-payment/<order_id>', views.payment_complete, name='complete_payment'),
     path('withdraw-request/', views.withdraw_request, name='withdraw_request'),
     path('confirm-withdraw/<pk>', views.confirm_withdraw, name='confirm_withdraw'),
     path('all-withdraw/', views.all_withdraw, name='all_withdraw'),
     path('all-deposits/', views.all_deposts_list, name='all_deposits'),
     path('all-payments/', views.all_payment_list, name='all_payments'),
     path('pending-payments/', views.pending_payment_list, name='pending_payments'),
     path('all-transactions/', views.all_transaction_list, name='all_transactions')
]