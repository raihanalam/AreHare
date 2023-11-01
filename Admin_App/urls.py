from unicodedata import name
from django.urls import path,include
from . import views

app_name = 'Admin_App'

urlpatterns = [
    path('profile-verfication-list/', views.profile_verification_list , name='profile_verification_list'),
    path('verfication-action-verify/<pk>/', views.verification_action_verify , name='verification_action_verify'),
    path('verfication-action-reject/<pk>/', views.verification_action_reject , name='verification_action_reject'),
]