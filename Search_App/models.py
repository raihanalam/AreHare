from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Search_History(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_search', null =True, default=None)
     keyword = models.CharField(max_length=200)
     ip = models.CharField(max_length=100,blank=True)
     browser = models.CharField(max_length=1024,blank=True)
     #results = models.ManyToManyField(#)
     time = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.keyword