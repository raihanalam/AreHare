
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
import uuid

from Work_App.models import Order

# Create your models here.
class Currency(models.Model):
     country_name = models.CharField(max_length=20)
     iso_code = models.CharField(max_length=3)
     symbol = models.CharField(max_length=20)
     cuurent_rate = models.FloatField(default=0)


     def __str__(self):
          return self.iso_code
     
class UserWallet(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_main_wallet')
     identity_type = models.CharField(max_length=100, null=True)
     identity_number = models.CharField(max_length=100, null=True)
     identity_image = models.ImageField(upload_to='identity_image', null=True)
     currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_user', null=True, blank=True)
     active = models.BooleanField(default=False)
     created_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.user

class Wallet(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="user_wallet")
     u_w = models.OneToOneField(UserWallet,on_delete=models.CASCADE, related_name='user_fixed_wallet')

     balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
     currency = models.CharField(max_length=3)

     def credit(self, amount):
          self.balance = self.balance + amount
          return True

     def debit(self, amount):
          if self.balance >= amount:
               self.balance = self.balance - amount
               return True

          else: return False
     
     def __str__(self):
        return f"{self.user.username}'s E-Wallet"
     



class Deposits(models.Model):

     payment_methods = (
          ('sslcommerz', 'SSLCommerz'),
          
     )

     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
     reference = models.TextField(max_length=264, verbose_name='Reference')
     amount = models.IntegerField(default=0)
     method = models.CharField(choices = payment_methods,max_length=20, default='sslcommerz')
     payment_type = models.CharField(max_length=100, blank=True)
     val_id = models.CharField(max_length=100) 
     trans_id  = models.CharField(max_length=100)
     success = models.BooleanField(default=False)
     created_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-created_date']


class PendingPayment(models.Model):
     user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_pending_payments')
     order_id = models.ForeignKey(Order, on_delete= models.CASCADE)
     amount = models.BigIntegerField(default=0)
     on_q = models.BooleanField(default=True)
     confirmation = models.BooleanField(default=False)
     success = models.BooleanField(default=False)
     created_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-created_date']


class Payment(models.Model):
     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_sender')
     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_receiver')
     amount = models.BigIntegerField(default=0)
     success_url = models.BooleanField(default=False)
     created_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-created_date']

class Transaction(models.Model):

     wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE, related_name='wallet_transaction')

     TRANSACTION_TYPES = (
          ('CREDIT', 'Credit'),
          ('DEBIT', 'Debit'),
     )
     transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
     transaction_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     timestamp = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"{self.transaction_type} - {self.amount}"

     class Meta:
          ordering = ['-timestamp']



class WithdrwalRequest(models.Model):
     method_choices =(
          ("bank", "Bank"),
          ("bkash", "Bkash"),
          ("nagad", "Nagad"),
     )
     status_choice = (
          ("pending", "Pending"),
          ("processing", "Processing"),
          ("success", "Success")
     )
     
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user_withdraw_request' )
     wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
     reference = models.CharField(max_length=50, blank=False)
     
     method = models.CharField(
        max_length=10,
        choices=method_choices,
        default= 'bank',
     )
     status = models.CharField( 
          max_length=10,
          choices=status_choice,
          default= 'pending',
     )
     account_number = models.CharField(max_length=20)
     
     amount = models.BigIntegerField(default=0)
     receivable_amount = models.FloatField(default=0)
     confirms = models.BooleanField(default=False, verbose_name='I accept terms and condition!')
     complete = models.BooleanField(default=False)
     network_fee = models.IntegerField(default=0)
     created_date = models.DateTimeField(auto_now_add=True)

     def calculate_network_fee(self):
          self.network_fee = (self.amount/100)*10
          self.receivable_amount = self.amount - self.network_fee

          return True


     class Meta:
          ordering = ['-created_date']




