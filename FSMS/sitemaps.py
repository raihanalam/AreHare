from django.contrib.sitemaps import Sitemap
from Main_App.models import Port

class PortSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Port.objects.all()
    
    def lastmod(self, obj):
          return obj.update_date
    
    def location(self, item):
         return item.get_absolute_url()
