from django.contrib import sitemaps
from django.urls import reverse
from store.models import Material

class FilamentSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Material.objects.all()

