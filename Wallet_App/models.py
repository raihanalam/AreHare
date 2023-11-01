
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings

from Work_App.models import Order

# Create your models here.
class UserWallet(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_main_wallet')
     identity_type = models.CharField(max_length=100)
     identity_number = models.CharField(max_length=100)
     identity_image = models.ImageField(upload_to='identity_image')

     country = models.CharField(verbose_name='Your country',max_length=100)
     active = models.BooleanField(default=False)
     created_date = models.DateTimeField(auto_now_add=True)


     def is_fully_filled(self):
          fields_names = [f.name for f in self._meta.get_fields()]

          for field_name in fields_names:
               value = getattr(self,field_name)
               if value is None or value=='':
                    return False
          return True 

# @receiver(post_save, sender=User)
# def created_wallet(sender,instance, created, **kwargs):
#      if created:
#           Wallet.objects.create(user= instance)

# @receiver(post_save,sender=User)
# def save_wallet(sender,instance,**kwargs):
#      instance.wallet.save()

class Wallet(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="user_wallet")
     u_w = models.OneToOneField(UserWallet,on_delete=models.CASCADE, related_name='user_fixed_wallet')

     key = models.CharField(max_length=30)
     balance = models.BigIntegerField(default=0)
     currency = models.CharField(max_length=20)
     created_date = models.DateTimeField(auto_now_add=True)


     def deposit(self, amount):
          self.balance = self.balance + amount
          return True

     def pay(self, amount):
          if self.balance >= amount:
               self.balance = self.balance - amount
               return True

          else: return False
               
     def withdraw(self):
          pass


class Deposits(models.Model):

     payment_methods = (
          ('sslcommerz', 'SSLCommerz'),
          ('paypal', 'PayPal')
          
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
     description = models.TextField(max_length=200)
     type = models.CharField(max_length=50)
     txn_id = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     confirms = models.BooleanField(default=False)
     amount = models.BigIntegerField(default=0)
     network_fee = models.BigIntegerField(default=0)
     created_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-created_date']




class WithdrwalRequest(models.Model):
     method_choices =(
          ("bank", "Bank"),
          ("bkash", "Bkash"),
          ("nagad", "Nagad"),
          ("paypal", "Paypal"),
          ("strip", "Strip"),
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
          self.network_fee = (self.amount/100)*9
          self.receivable_amount = self.amount - self.network_fee

          return True


     class Meta:
          ordering = ['-created_date']



class Currency(models.Model):
     cuurency_name = models.CharField(max_length=20)
     short_name = models.CharField(max_length=10)
     symbol = models.CharField(max_length=20)
     cuurent_rate = models.IntegerField(default=0)


     def __str__(self):

          return self.short_name
