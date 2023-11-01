from django.urls import path,include
from . import views

app_name = 'Account_App'

urlpatterns = [
    path('signup/',views.sign_up,name='signup'),
    path('signin/',views.sign_in,name='signin'),
    path('signout/',views.sign_out,name='signout'),
    path('user/',views.user_profile,name='profile'),
    path('change-profile/',views.change_profile,name='change_profile'),
    path('password/',views.change_password,name='change_password'),
    path('add-picture/',views.add_pro_pic,name='add_pro_pic'),
    path('change-picture/',views.change_pro_pic,name='change_pro_pic'),
    path('change-profile-info',views.user_profile_change, name='user_profile_chnage'),
    path('settings/',views.settings,name='settings'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('verification/',views.profile_verification, name='profile_verification'),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),

    path('social/signup/', views.signup_redirect, name='signup_redirect'),
    path('profile/<username>',views.user_profile_view, name= 'user_profile'),
]