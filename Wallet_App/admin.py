from django.contrib import admin
from .models import Transaction, UserWallet, Wallet, Deposits, PendingPayment,Payment, WithdrwalRequest, Currency

# Register your models here.
admin.site.register(UserWallet)
admin.site.register(Wallet)
admin.site.register(Deposits)
admin.site.register(Transaction)
admin.site.register(PendingPayment)
admin.site.register(Payment)
admin.site.register(WithdrwalRequest)
admin.site.register(Currency)