from django.shortcuts import render
from .models import NavigationItem, PageModel
from django.contrib.auth.models import User
from Account_App.models import UserProfile
from Main_App.models import Port
from Main_App.forms import PublicPostForm
from Main_App.models import Partners


# Create your views here.
def index(request):
    customer = UserProfile.objects.filter(role='customer')
    ports = Port.objects.filter(active=True).order_by('-rating')
    public_post_form = PublicPostForm()
    partners = Partners.objects.all()

    
    return render(request,'index.html', context={'customer_list': customer, 'ports': ports, 'public_post_form':public_post_form, 'partners': partners})

def page_view(request, slug):
    
    top_level_items = NavigationItem.objects.filter(parent__isnull=True).prefetch_related('children')
    page_data = PageModel.objects.get(slug=slug)

    return render(request, 'page_view.html', {'page_data': page_data, 'navigation_items':top_level_items})