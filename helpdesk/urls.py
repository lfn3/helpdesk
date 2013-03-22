from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('survey.urls', namespace='survey', app_name='survey')),
)

handler404 = 'survey.urls.index'