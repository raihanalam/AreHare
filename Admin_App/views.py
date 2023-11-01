from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from Account_App.models import UserProfile

from Account_App.models import Verification

# Create your views here.
def profile_verification_list(request):
     if request.user.user_profile.role == 'admin':
          verifications = Verification.objects.filter()

          dict = {'verifications': verifications}
          return render(request, 'profile_verification.html', context=dict)
     
def verification_action_verify(request, pk):
     if request.user.user_profile.role == 'admin':
          verification = Verification.objects.get(pk=pk)
          userProfile = UserProfile.objects.get(user=verification.user)
          
          if verification.status == 'Pending' or verification.status == 'Rejected':
               verification.status= 'Verified'
               userProfile.verified = True
               userProfile.save()
               verification.save()
     else:
          messages.warning(request, 'You are not able to do this.')

     
     return HttpResponseRedirect(reverse('Admin_App:profile_verification_list'))

def verification_action_reject(request, pk):
     if request.user.user_profile.role == 'admin':
          verification = Verification.objects.get(pk=pk)
          
          if verification.status == 'Pending':
               verification.status= 'Rejected'
               verification.user.user_profile.verified = False
               verification.save()
     else:
          messages.warning(request, 'You are not able to do this.')

     return HttpResponseRedirect(reverse('Admin_App:profile_verification_list'))
          

