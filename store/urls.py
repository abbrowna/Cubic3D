"""
Definition of urls for store.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import FilamentSitemap, StaticViewSitemap
from store import forms, views
from django.views.generic.base import TemplateView


from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

sitemaps = {
    'filament':FilamentSitemap,
    'static':StaticViewSitemap
}


app_name = 'store'
urlpatterns = [
    path('', views.filamentLanding, name='filamentHome'),
    #path('filament', views.filamentLanding, name='filamentHome'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='store/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('filament/<str:diameter>/<str:material>/', views.filament, name='filament'),
    path('ajax/addCart/', views.addToCart, name='addTocart'),
    path('ajax/removeCart/', views.removeFromCart, name='removeFromCart'),
    path('ajax/setPaid/', views.setPaid, name='setPaid'),
    path('ajax/setDelivered/', views.setDelievered, name='setDelievered'),
    path('ajax/updateCart/', views.updateCart, name='updateCart'),
    path('filament/cart/', views.cart, name='cart'),
    path('filament/checkout/', views.checkout, name='checkout'),
    path('ajax/updateDelivery', views.updateDelivery, name='updateDelivery'),
    path('filament/order-review', views.orderReview, name='orderReview'),
    path('filament/how-to', views.howTo, name='howTo'),
    path('myadmin/', views.myadmin, name='myadmin'),
    path('myadmin/release-stock', views.releaseStock, name='releaseStock'),
    path('myadmin/pre-orders', views.preOrders, name='preOrders'),
    path('myadmin/pending-orders', views.pendingOrders, name='pendingOrders'),
    path('myadmin/completed-orders', views.completedOrders, name='completedOrders'),
    #path('api/callback', views.apiCallback, name='apiCallback'),
    #path('api/Express', views.mpesaExpress, name='mpesaExpress'),
    path('djga/', include('google_analytics.urls')),
    
    #temporary email construction
    path('email/emailviewer', views.emailViewer, name='emailViewer'),
    #robots.txt
    path('robots.txt/',
        TemplateView.as_view(template_name='Robots.txt', content_type='text/plain'),
    ),

    #Authentication
    path('accounts/login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form= forms.BootstrapAuthenticationForm,
            extra_context=
            {
                'title': 'Log in',
                'year': datetime.now().year
            }
            ),name='login'
        ),
    path('signup/',views.signup, name='signup'),
    path('signup/verification/<user_email>',views.pending_verification, name='pending_verification'),
    path('verification/', include('verify_email.urls')),
    path('logout/',LogoutView.as_view(), name='logout'),
    
    path('accounts/overview/', views.accountOverview, name='acc_overview'),
    path('accounts/profile/', views.editProfile, name='edit_profile'),
    path('accounts/password_reset/',
        PasswordResetView.as_view(
            template_name='registration/pass_reset_form.html',
            html_email_template_name='registration/pass_reset_email.html',
            form_class=forms.PasswordResetFormCaptcha,
            from_email='support@cubic3d.co.ke',
        ),name='password_reset'),

    path('accounts/password_reset_done/',
        PasswordResetDoneView.as_view(
            template_name='registration/pass_reset_done.html',
        ),name='password_reset_done'),

    path('accounts/password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/pass_reset_confirm.html',
        ),name='password_reset_confirm'),

    path('accounts/password_reset_complete/',
        PasswordResetCompleteView.as_view(
            template_name='registration/pass_reset_complete.html',
        ),name='password_reset_complete'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
