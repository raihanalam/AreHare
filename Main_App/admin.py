from django.contrib import admin
from .models import Category, PortImageGallery ,Post,Port,Bid,Hire, ReviewRating, Partners, PublicPost

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Port)
admin.site.register(PortImageGallery)
admin.site.register(Bid),
admin.site.register(Hire)
admin.site.register(ReviewRating)
admin.site.register(Partners)
admin.site.register(PublicPost)