from django.db import models

# Create your models here.


class Partners(models.Model):
     partner_name = models.CharField(max_length=64)
     partner_logo = models.ImageField(upload_to='partners')
