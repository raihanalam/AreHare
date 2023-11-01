from unicodedata import name
from django.urls import path,include
from . import views

app_name = 'Dashboard_App'

urlpatterns = [
    path('', views.dashboard , name='dashboard'),
]