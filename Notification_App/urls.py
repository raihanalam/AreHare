from django import views
from django.urls import path
from . import views

app_name = 'Notification_App'

urlpatterns = [
     path('', views.notification, name='notification'),
     path('mark-all-read', views.mark_all_read, name='mark_all_read')
]