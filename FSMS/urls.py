
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PortSitemap

sitemaps = {
    'port': PortSitemap,
    # Add more sitemaps if needed
}


urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('arehare-super-admin/', admin.site.urls),
    path('',views.index,name='index'),
    # path('account/',include('account.urls')),
    #path('home/',include('home.urls')),
    path('account/',include('Account_App.urls')),
    path('home/',include('Main_App.urls')),
    path('dashboard/',include('Dashboard_App.urls')),
    path('chatbox/',include('Message_App.urls')),
    path('work/',include('Work_App.urls')),
    path('wallet/',include('Wallet_App.urls')),
    path('notifications/',include('Notification_App.urls')),
    path('search/',include('Search_App.urls')),
    path('inbox/notifications/',include('notifications.urls', namespace='notifications')),
    path('custom-admin/', include('Admin_App.urls')),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
