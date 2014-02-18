from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'personal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'personal.views.home'),
    (r'^shopped/', include('shopped.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
