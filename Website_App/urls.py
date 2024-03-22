from django.urls import path, include
from Website_App.views import page_view, index

urlpatterns = [

     path('', index, name='index'),
     path('page/<slug>/', page_view, name='page_view'),
]