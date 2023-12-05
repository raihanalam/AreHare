from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'Main_App'

urlpatterns = [
    path('',views.home, name='home_page'),

    #All Port Related Urls
    path('port-job',views.CreatePort.as_view(), name='create_port'),
    path('port-details/<slug>',views.port_details, name='port_details'),
    path('cancel-hire-request/<pk>',views.cancel_hire_rquest,name="cancel_hire"),
    path('my-port/',views.MyPorts.as_view(),name='my_ports'),
    path('edit-port/<pk>',views.UpdatePort.as_view(),name='edit_port'),
    path('submit_review/<int:freelancer>/', views.submit_review, name='submit_review'),
    
    path('active-port-list/',views.active_port_list, name='active_port_list'),
    path('deactivated-port-list/',views.deactivated_port_list, name='deactivated_port_list'),
    path('delete-port/<pk>',views.delete_port,name="delete_port"),
    path('deactivate-port/<pk>',views.deactivate_port,name="deactivate_port"),
    path('activate-port/<pk>',views.activate_port,name="activate_port"),
    path('all-hire-requests', views.all_hires_requests, name='all_hires'),

    #All Post Related Urls
    path('post-job',views.CreatePost.as_view(), name='create_post'),
    path('post-details/<slug>',views.post_details, name='post_details'),
    path('unbid/<pk>',views.unbid,name="unbid_post"),
    path('bid-review/<pk>', views.review_bid, name='review_bid'),
    path('my-post/',views.MyPosts.as_view(),name='my_posts'),
    path('edit-post/<pk>',views.UpdatePost.as_view(),name='edit_post'),
    path('active-post-list/',views.active_post_list, name='active_post_list'),
    path('deactivated-post-list/',views.deactivated_post_list, name='deactivated_post_list'),
    path('delete-post/<pk>',views.delete_post,name="delete_post"),
    path('deactivate-post/<pk>',views.deactivate_post,name="deactivate_post"),
    path('activate-post/<pk>',views.activate_post,name="activate_post"),
    path('all-bids', views.all_bids, name='all_bids'),

    path('load-more',views.load_more,name='load-more'),
    path('quick-quize', views.quick_quize, name='quick_quize'),
    path('port-bulk-image-upload/<port_id>',views.port_bulk_image_upload, name='port_bulk_image_upload'),
    path('port-gallery-image-delete/<img_id>', views.delete_port_gallery_image, name='delete_port_gallery_image'),
]