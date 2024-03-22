
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings
from pkg_resources import require
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify


#Getting custom base User model
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        
class Category(models.Model):
     title = models.CharField(max_length=50,verbose_name="Category title...")
     created= models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.title

     class Meta:
          ordering = ['-created']
          verbose_name_plural = "Categories"


class Post(models.Model):
     post_category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='categorized_post')
     post_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='post_author')
     
     post_title = models.CharField(max_length=264,verbose_name="Post Title")
     slug = models.SlugField(max_length=200,unique=True)
     required_skills = models.CharField(max_length=50,verbose_name="Required Skill")
     keywords= models.CharField(max_length=264, verbose_name = 'Keywords', blank=True, null=True)
     post_description = RichTextField(verbose_name="Write your job description here...")
     deadline = models.DateField(verbose_name="Deadline...",)
     post_image = models.ImageField(upload_to='post_images', verbose_name="Image", blank=True, null=True)
     active = models.BooleanField(default=True)
     budget_amount = models.PositiveIntegerField(verbose_name="Budget amount..")
     publish_date = models.DateTimeField(auto_now_add=True)
     update_date = models.DateTimeField(auto_now=True)

     class Meta:
          ordering = ['-publish_date']

     def __str__(self):
         return self.post_title

class Port(models.Model):
     port_category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='port_category')
     port_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='port_author')

     port_title = models.CharField(max_length=264,verbose_name="Port Title")
     slug = models.SlugField(max_length=528,unique=True)
     expert =models.CharField(max_length=264,verbose_name="Your expertness")
     skills = models.CharField(max_length=264, verbose_name='Skills')
     keywords = models.CharField(max_length=264,verbose_name="Keywords")
     port_description = RichTextField(verbose_name="Write about you here...")
     port_image = models.ImageField(upload_to='port_images', verbose_name="Image")
     active = models.BooleanField(blank=True)
     rate_amount = models.PositiveIntegerField(verbose_name="Order rate")
     publish_date = models.DateTimeField(auto_now_add=True)
     update_date = models.DateTimeField(auto_now=True)

     #Ratings
     rating = models.FloatField(default=0)

     class Meta:
          ordering = ['-publish_date']
     
     def __str__(self):
         return self.port_title
     

     def get_absolute_url(self):
          return reverse('Main_App:port_details', kwargs={'slug': self.slug})


     
     @property
     def imageURL(self):
          try:
               url = self.port_image.url
          except:
               url = ''
               print('URL:', url)
               return url

     


class Bid(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user_bid')
     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_bid')
     port = models.ForeignKey(Port,on_delete=models.CASCADE,related_name='port_bid')
     
     bid_note = models.TextField(verbose_name="Send note...",)
     bid_amount = models.IntegerField(verbose_name="Bid amount...")
     STATUS = [
          ("bidded", "Bidded"),
          ("canceled","Canceled" ),
          ("reviewed", "Reviewed"),
          ("accepted", "Accepted"),
     ]
     status = models.CharField(choices=STATUS, max_length=10, default='bidded')
     bid_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-bid_date']

     def __str__(self):
          return self.bid_note


class Hire(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user_hire')
     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_hire', blank=True, null=True)
     port = models.ForeignKey(Port,on_delete=models.CASCADE,related_name='port_hire')


     hire_message = models.TextField(verbose_name="Write about your work...",)
     hire_amount = models.IntegerField(verbose_name="Budget amount...")
     hire_date = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['-hire_date']

     def __str__(self):
          return self.hire_message


class ReviewRating(models.Model):

     freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='freelancer_profile_ratings')
     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_given_ratings')
     
     review = models.CharField(max_length=500)
     rating = models.FloatField()

     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)


class PortImageGallery(models.Model):
     port = models.ForeignKey(Port, default=None, on_delete=models.CASCADE, related_name='port_bulk_images')
     image = models.ImageField(upload_to='port_images/', max_length=255)

     def __str__(self):
        return self.port.port_title
     

     class Meta:
        verbose_name = 'portimagegallery'
        verbose_name_plural = 'port image gallery'


     @property
     def imageURL(self):
          try:
               url = self.image.url
          except:
               url = ''
          print('URL:', url)
          return url



class SavedPort(models.Model):
     port_id = models.ForeignKey(Port, on_delete=models.CASCADE)
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PublicPost(models.Model):
     category = models.ForeignKey(Category, related_name='category_public_post', on_delete=models.CASCADE, blank=True, null=True)
     full_name = models.CharField(verbose_name='Full Name', max_length=30)

     email = models.CharField(verbose_name='Email', max_length=64)
     phone = models.CharField(verbose_name='Phone', max_length=20)
     

     title = models.CharField(verbose_name='Title', max_length=164)
     description = models.TextField(verbose_name='Description', max_length=500)

     files = models.FileField(
          verbose_name='Attachment', upload_to='work_files',

          null=True, blank= True
     )
     
     STATUS_CHOICES = (
          ('POSTED', 'Posted'),
          ('PROCESSED', 'Processed'),
          ('SUCCEED', 'Succeed'),
          ('CANCELED', 'Canceled')
     )
     status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='POSTED')

class Partners(models.Model):
     name = models.CharField(max_length=255, verbose_name = 'Name')
     logo = models.ImageField(upload_to='partners')
     
     # category = models.ForeignKey(Category, related_name = 'partner_category', on_delete = models.CASCADE, blank=True, null=True)
     address = models.CharField(max_length=255, verbose_name = 'Address', blank=True, null=True)
