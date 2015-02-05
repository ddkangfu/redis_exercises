from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'redis_exercises.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.MainView.as_view(), name='home'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout'),
    
    url(r'^admin/', include(admin.site.urls)),
)
