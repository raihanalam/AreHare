from django.contrib import admin
from .models import User, UserProfile, Verification

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Verification)

admin.site.site_header = 'amarKaz Administration'
