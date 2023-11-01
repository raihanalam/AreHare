from django.contrib import admin
from .models import Offer, Order, RunningWork, CompleteWork, RunningWorkFiles, Report

# Register your models here.
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(RunningWork)
admin.site.register(CompleteWork)
admin.site.register(RunningWorkFiles)
admin.site.register(Report)