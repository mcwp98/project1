from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^analyzed/(?P<photo_id>\d+)/$', 'shopped.views.analyzed'),
    url(r'^$', 'shopped.views.create'),
)
