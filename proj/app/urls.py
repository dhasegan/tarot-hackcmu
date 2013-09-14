from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'app.views.login'),

    url(r'^discover/', 'app.views.discover'),
    url(r'^dashboard/', 'app.views.dashboard'),

    url(r'^discover/add_question', 'app.views.add_question')
    
)
