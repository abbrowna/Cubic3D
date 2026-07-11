from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):

    _priorities = {
        'home': 1.0,
        'about': 0.8,
        'materials': 0.8,
        'gallery': 0.7,
        'contact': 0.6,
        'upload': 0.5,
    }
    _changefreqs = {
        'home': 'weekly',
        'about': 'monthly',
        'materials': 'weekly',
        'gallery': 'weekly',
        'contact': 'monthly',
        'upload': 'monthly',
    }

    def items(self):
        return ['home', 'about', 'materials', 'contact', 'gallery', 'upload']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._priorities.get(item, 0.5)

    def changefreq(self, item):
        return self._changefreqs.get(item, 'monthly')