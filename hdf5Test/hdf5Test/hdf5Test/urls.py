"""
Definition of urls for h5Test.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    
    url(r'^dirFileRead$', app.views.dirFileReadFnc, name='dirFileReadFnc'),
    url(r'^getImageByDir$', app.views.getImageByDirFnc, name='getImageByDirFnc'),
    url(r'^crawling$', app.views.crawling, name='crawling'),
    url(r'^crawlerResult', app.views.crawlerResultPage, name='crawlerResultPage'),

    #ajax post
    url(r'^getImage/$', app.views.getImageFnc, name='getImageFnc'),
    url(r'^getCrawlerResultList$', app.views.getCrawlerResultListFnc, name='getCrawlerResultListFnc'),
    url(r'^webcrawlerStart', app.views.webcrawlerStart, name='webcrawlerStart'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
