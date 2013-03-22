from django.conf.urls import patterns, url
from survey import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^(?P<code>\w+)/$', views.fill, name='fill'),
	url(r'^(?P<code>\w+)/post$', views.post, name='post'),
	)