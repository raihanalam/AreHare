from unicodedata import category
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from Account_App.models import UserProfile
from Main_App.models import Port
from Main_App.forms import PublicPostForm


# Create your views here.
def index(request):
    customer = UserProfile.objects.filter(role='customer')
    ports = Port.objects.filter(active=True).order_by('-rating')
    public_post_form = PublicPostForm()

    
    return render(request,'index.html', context={'customer_list': customer, 'ports': ports, 'public_post_form':public_post_form})