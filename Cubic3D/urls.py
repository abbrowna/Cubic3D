"""
Definition of urls for Cubic3D.
"""

from datetime import datetime
from django.conf.urls import url
from django.urls import path
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

import app.forms
import app.views
from app import views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('materials/',app.views.materials, name='materials'),
    path('gallery/',views.gallery, name='gallery'),
    path('ajax/load-colors/',views.load_colors, name='ajax_load_colors'),
    path('getting_started/upload/',views.upload, name='upload'),
    path('getting_started/quote_upload/',views.def_quote, name='def_quote'),
    path('getting_started/review_n_info/',app.views.review_n_info, name='review_n_info'),
    path('getting_started/quote_review/',app.views.quote_review, name='quote_review'),
    path('getting_started/review_n_info/cancel_print/',app.views.cancel, name='cancel'),
    path('getting_started/quote_review/quote_finish/',app.views.delquote, name='delquote'),
    path('getting_started/thanks/',app.views.thanks, name='thanks'),
    path('printrequests/confirm/<thing_id>/',app.views.confirm_print, name='confirm'),
    path('my_admin/',app.views.myadmin, name='myadmin'),
    path('my_admin/printrequest/download/<path>/',app.views.download, name='download'),
    path('my_admin/orders/set_printed/<id>/',app.views.set_printed, name='set_printed'),
    path('my_admin/printrequests/delete_file/<requestid>/',app.views.delete_file, name='delete_file'),
    path('my_admin/printrequests/accept_or_reject/<requestid>/',app.views.accept_or_reject, name='accept_or_reject'),
    path('my_admin/printrequests/',app.views.printrequests, name='printrequests'),
    path('my_admin/printrequests/group/' , app.views.grouped_requests, name='grouped_requests'),
    path('my_admin/printrequests/group/remove/<requestid>/', app.views.remove_from_group, name='remove_from_group'),
    path('my_admin/printrequests/pending/', app.views.pending_confirmation, name='pending_confirmation'),
    path('my_admin/orders/printed/', app.views.printed, name='printed'),
    path('my_admin/orders/completed/', app.views.completed_orders, name='completed'),
    path('my_admin/orders/old_completed/', app.views.old_sys_orders, name='old_sys_orders'),
    path('my_admin/orders/printed/receipt/<invoice_id>/<orderlist>/', app.views.send_receipt, name='send_receipt'),
    path('my_admin/orders/pending/',app.views.orders, name='orders'),
    path('my_admin/user_profiles/', app.views.user_profiles, name='user_profiles'),
    path('accounts/change_profile/', app.views.change_profile, name='change_profile'),
    
    #temporary path to set username as email
    path('email_is_username/', app.views.email_is_username, name='email_is_username'),

    path('accounts/login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form= app.forms.BootstrapAuthenticationForm,
            extra_context=
            {
                'title': 'Log in',
                'year': datetime.now().year
            }
            ),name='login'
        ),   
    path('signup/',app.views.signup, name='signup'),
    path('logout/',django.contrib.auth.views.LogoutView.as_view(), name='logout'),
    
    path('accounts/password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='registration/pass_reset_form.html',
            html_email_template_name='registration/pass_reset_email.html',
            from_email='support@cubic3d.co.ke',
        ),name='password_reset'),

    path('accounts/password_reset_done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='registration/pass_reset_done.html',
        ),name='password_reset_done'),

    path('accounts/password_reset_confirm/<uidb64>/<token>/',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='registration/pass_reset_confirm.html',
        ),name='password_reset_confirm'),

    path('accounts/password_reset_complete/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='registration/pass_reset_complete.html',
        ),name='password_reset_complete'),
    
    path('email/pdf/',app.views.pdf, name='pdf'),
    
    #path('accounts/', include('django.contrib.auth.urls')),
    
    path('viewer', TemplateView.as_view(template_name="app/stlviewer.html"),name='viewer'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin',admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
