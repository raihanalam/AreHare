from django.db import models
from django.contrib.auth.models import User

from Main_App.models import Port
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

class Offer(models.Model):
     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name="customer_offer")
     freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="freelancer_offer")

     description = models.TextField(max_length=500)
     amount = models.IntegerField(verbose_name="Offer ammount ")
     expected_time = models.DateField(verbose_name="Expected submission date...",)
     support = models.IntegerField(verbose_name="How many times support will give?")

     OFFER_STATES = [
          ('Pending', 'Pending'),
          ('Accepted', 'Accepted'),
          ('Rejected', 'Rejected')
     ]

     status = models.CharField(choices=OFFER_STATES,max_length=10, default='Pending')

     date_created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return '{} - {} : {}'.format(self.id, self.customer, self.freelancer)

     class Meta:
          ordering = ['-date_created']

class Order(models.Model):
     offer_id = models.OneToOneField(Offer,on_delete=models.CASCADE, related_name='ordered_offer')
     freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="freelancer_order")
     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="customer_order")
     instruction = models.TextField(verbose_name="Instructions...")
     amount = models.FloatField(default=0)
     deadline = models.DateTimeField(verbose_name="Last date of submission...")

     ORDER_STATES = [
          ('Created', 'Created'),
          ('Placed', 'Placed'),
          ('Canceled', 'Canceled'),

          ('Accepted', 'Accepted'),
          ('Rejected', 'Rejected'),

          ('Running', 'Running'),
          ('Completed', 'Completed')
     ]
     status = models.CharField(choices= ORDER_STATES,max_length=10, default='Created')

     PAYEMENT_STATES = [
          ('Checkout', 'Checkout'),
          ('Pending', 'Pending'),
          ('Succeed', 'Succeed'),
     ]
     payment_status = models.CharField(choices=PAYEMENT_STATES,max_length=10, default='Checkout')
     
     created = models.DateTimeField(auto_now_add=True)

     def get_totals(self):
          return self.amount

     def __str__(self):
          return '{} - {} : {} -{}'.format(self.id, self.customer.username, self.freelancer.username, self.offer_id.id)

     class Meta:
          ordering = ['-created']

class RunningWork(models.Model):
     order_id = models.OneToOneField(Order,on_delete=models.CASCADE, related_name='running_work')
     freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="freelancer_running_work")
     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="customer_running_work")
     running = models.BooleanField(default=False, verbose_name="Yes I'm ready to start this work.")
     work_track = models.IntegerField()
     completed = models.BooleanField(default=False)
     canceled = models.BooleanField(default=False)
     date_created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return '{} - {} : {} - {}'.format(self.id, self.customer.username, self.freelancer.username, self.order_id)
     

     class Meta:
          ordering = ['-date_created']
          
class RunningWorkFiles(models.Model):
     work_id = models.ForeignKey(RunningWork, on_delete=models.CASCADE, related_name= 'work_files')
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
     file_name = models.CharField(max_length=128)
     file = models.FileField(verbose_name='Work File', upload_to='work_files')
     date_created = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-date_created']

     def __str__(self):
          return self.file_name

class CompleteWork(models.Model):
     order_id = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='complete_order')
     work_id = models.OneToOneField(RunningWork, on_delete=models.CASCADE, related_name='complete_work')
     freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="freelancer_complete_order")
     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="customer_complete_order")
     freelancer_confirmation = models.BooleanField(default=False)
     customer_confirmation = models.BooleanField(default=False)
     completed = models.BooleanField(default=False)
     date_created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return '{} - {} : {} - {}'.format(self.id, self.customer.username, self.freelancer.username, self.id, self.order_id, self.work_id)

     class Meta:
          ordering = ['-date_created']

     class Meta:
          ordering = ['-date_created']


class Report(models.Model):
     user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="user_report")
     work_id = models.ForeignKey(RunningWork, on_delete=models.CASCADE, related_name="work_report")
     subject = models.CharField(max_length=264)
     body = models.CharField(max_length=500)

class CanceledWork(models.Model):
     pass
