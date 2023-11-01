from django.db import models

#To create a custom user model and admin pannel
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User


#To automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

from Main_App.models import ReviewRating
from django.db.models import Avg, Count
from django.utils.timezone import datetime

from django_countries.fields import CountryField

# Create your models here.

class MyUserManager(BaseUserManager):
     '''A custom manager to deal with emails as unique identifier'''
     def _create_user(self,email,password, **extra_fields):
          """Create and save a user with a given email and password """

          if not email:
               raise ValueError("The Email must be set")
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields )
          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self, email, password, **extra_fileds):
          extra_fileds.setdefault('is_staff', True)
          extra_fileds.setdefault('is_superuser', True)
          extra_fileds.setdefault('is_active', True)

          if extra_fileds.get('is_staff') is not True:
               raise ValueError('Superuser must have is staff True')
          if extra_fileds.get('is_superuser') is not True:
               raise ValueError('Super user must have is superuser true.')
          return self._create_user(email, password, **extra_fileds)


class User(AbstractBaseUser,PermissionsMixin):
     username = models.CharField(max_length=264,unique=True, null=False)
     email = models.EmailField(unique=True, null=False)
     # role = models.CharField(max_length=10, null=False)

     is_staff = models.BooleanField(
          gettext_lazy('staff status'),
          default= False,
          help_text= gettext_lazy('Designates whether the user can log in this site')
     )

     is_active = models.BooleanField(
          gettext_lazy('active'),
          default = True,
          help_text = gettext_lazy('Designates whether this user should be treated as active. Unselect this insstead of deleting accounts')

     )
     USERNAME_FIELD = 'email'
     objects = MyUserManager()

     def __str__(self):
          return self.email

     def get__full_name(self):
          return self.email

     def get_short_name(self):
          return self.email


class UserProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile')
     full_name =  models.CharField(max_length=264, blank=True)
     role = models.CharField(max_length=10)
     dob = models.DateField(verbose_name="Date of birth", null=True, blank= True)

     
     profile_pic = models.ImageField(upload_to ='profile_pics',blank=True )
     
     verified = models.BooleanField(default=False)

     bio = models.TextField(max_length=500, blank=True)

     #Education
     university_name = models.CharField(max_length=1320, blank=True)
     degree = models.CharField(max_length=100, blank=True)

     #Company
     company_name = models.CharField(max_length=124, blank=True)
     designation = models.CharField(max_length=64, blank=True)


     #Address
     address_1 = models.CharField(max_length=300,blank=True)
     city = models.CharField(max_length=40,blank=True)
     zipcode = models.CharField(max_length=10,blank=True)
     
     # country = CountryField()
     country = models.CharField(max_length=50,blank=True)
     phone = models.CharField(max_length=20,blank=True)
     date_joined = models.DateTimeField(auto_now_add=True)

     def averageReview(self):
          reviews = ReviewRating.objects.filter(freelancer=self.user, status=True).aggregate(average=Avg('rating'))
          avg = 0
          if reviews['average'] is not None:
               avg = float(reviews['average'])
          return avg

     def countReview(self):
          reviews = ReviewRating.objects.filter(port=self.user, status=True).aggregate(count=Count('id'))
          count = 0
          if reviews['count'] is not None:
               count = int(reviews['count'])
          return count
          

     def is_fully_filled(self):
          fields_names = [f.name for f in self._meta.get_fields()]
          for field_name in fields_names:
               value = getattr(self,field_name)
               if value is None or value=='':
                    return False
          return True

     def __str__(self):
               return self.role +str(' ----- ')+ self.user.username + str("'s profile")

           
# @receiver(post_save, sender=User)
# def created_profile(sender,instance, created, **kwargs):
#      if created:
#           UserProfile.objects.create(user= instance)

# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#      instance.user_profile.save()

class Verification(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_verification')
     subject = models.CharField(max_length=264)
     application = models.TextField(max_length=500)
     STATUS_CHOICES = [('Pending', 'Pending'),('Verified', 'Verified'), ('Rejected', 'Rejected')]
     status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=200)
     verified = models.BooleanField(default=False)
     rejected=models.BooleanField(default=False)
     created = models.DateTimeField(auto_now_add=True)


     class Meta:
          ordering = ['-created']

