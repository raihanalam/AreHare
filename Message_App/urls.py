from django.urls import path
from . import views
app_name = 'Message_App'

urlpatterns = [
    path('', views.Inbox.as_view() , name='inbox'),
    path('room/<str:room_name>/', views.Room.as_view() , name='room'),
    path('join-chat/<str:f_username>/',views.join_chat, name="join_chat"),
    path('leave-box/<str:room_name>/',views.leave_chat, name="leave_chat"),
]