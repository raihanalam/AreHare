from django import views
from django.urls import path
from . import views

app_name = 'Work_App'

urlpatterns = [
     path('get-work-data', views.get_work_data, name='get_work_data'),

     path('cancel-order/<order_id>', views.cancel_order, name='cancel_order'),

     path('order/<pk>', views.place_order, name='place_order'),
     path('start-work/<pk>', views.start_work, name='start_work'),
     path('all-orders/', views.all_order, name='all_orders'),
     path('running-work/<order_id>', views.running_work, name='running_work'),
     path('complete-work/<pk>', views.complete_work, name='complete_work'),
     path('all-running-orders', views.all_running_orders, name='all_running_orders'),
     path('all-successfull-orders', views.all_succesfull_orders, name='all_successfull_orders'),
     path('push/<work_id>',views.push, name='work_push'),
     path('pop/<work_id>',views.pop, name='work_pop'),
     path('send_file/<work_id>',views.send_file, name='send_file'),
     path('give-report/<work_id>',views.give_report, name='give_report'),

     path('all-offers', views.all_offers, name='all_offers'),
     path('recent-offers', views.recent_oders, name='recent_offers'),
     path('recent-orders', views.recent_oders, name='recent_orders'),
     path('send-offer/<receiver>', views.send_offer, name='send_offer'),
     
]