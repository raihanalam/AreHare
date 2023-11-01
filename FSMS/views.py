from unicodedata import category
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from Account_App.models import UserProfile
from Main_App.models import Port

# Create your views here.
def index(request):
    customer = UserProfile.objects.filter(role='customer')
    ports = Port.objects.filter(active=True).order_by('-rating')
    
    return render(request,'index.html', context={'customer_list': customer, 'ports': ports})