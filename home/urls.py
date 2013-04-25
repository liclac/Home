from django.conf.urls import patterns, include, url
from views import *
from blog.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'home.views.home', name='home'),
	# url(r'^home/', include('home.foo.urls')),
	url(r'^$', HomeView.as_view(), name='home'),
	url(r'^blog/$', PostListView.as_view(), name='posts'),
	url(r'^blog/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post'),
	url(r'^blog/(?P<pk>\d+)/(?P<slug>[-\w]+)/', PostDetailView.as_view(), name='post'),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	url(r'^grappelli/', include('grappelli.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
