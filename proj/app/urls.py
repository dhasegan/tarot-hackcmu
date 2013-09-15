from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'app.views.signup'),
    url(r'^logout/', 'app.views.signout'),

    url(r'^$', 'app.views.discover'),
    url(r'^discover/', 'app.views.discover'),
    url(r'^dashboard/', 'app.views.dashboard'),

    url(r'^add_question$', 'app.views.add_question')
    
)
