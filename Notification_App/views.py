from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

# Create your views here.


def notification(request):

     return render(request, 'notifications.html')

@login_required
def mark_all_read(request):

     unread_notification = Notification.objects.filter(recipient=request.user, unread=True)

     for notif in unread_notification:
          notif.unread = False
          notif.save()
     
     return HttpResponseRedirect(reverse('Main_App:home_page'))
