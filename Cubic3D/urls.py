"""
Definition of urls for Cubic3D.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^gettingstarted/upload',app.views.upload, name='upload'),
    url(r'^gettingstarted/review_n_info',app.views.review_n_info, name='review_n_info'),
    url(r'^cancelprint',app.views.cancel, name='cancel'),
    url(r'^confirm/(?P<thing_id>[0-9]+)/$',app.views.confirm_print, name='confirm'),
    url(r'^download/(?P<path>.*)/$',app.views.download, name='download'),
    url(r'^setprinted/(?P<id>.*)/$',app.views.set_printed, name='set_printed'),
    url(r'^gettingstarted/thanks',app.views.thanks, name='thanks'),
    url(r'^thingiverse',app.views.thingiverse, name='thingiverse'),
    url(r'^materials',app.views.materials, name='materials'),
    url(r'^gallery',app.views.gallery, name='gallery'),
    url(r'^send_confirmation_link',app.views.send_confirm_link, name='send_confirm_link'),
    url(r'^orders',app.views.orders, name='orders'),
    url(r'^accounts/login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'registration/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        }, 
        name='mylogin'),
    url(r'^gettingstarted/login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/startlogin.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Getting Started:First, let\'s get you Logged in',
                'year': datetime.now().year,
            }
        }, 
        name='startlogin'),
    url(r'^signup/$',app.views.signup, name='signup'),
    url(r'^gettingstarted/signup/$',app.views.startsignup, name='startsignup'),
    url(r'^logout$',django.contrib.auth.views.logout,
        {
            'next_page': '/',
        }, 
        name='logout'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^viewer/', TemplateView.as_view(template_name="app\stlviewer.html"),
                   name='viewer'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
