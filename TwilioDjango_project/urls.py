from django.conf.urls import patterns, include, url
from django.contrib import admin
from TwilioServer import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TwilioDjango_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
)
