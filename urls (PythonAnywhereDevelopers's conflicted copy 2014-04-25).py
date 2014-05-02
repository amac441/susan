from django.conf.urls import url
from django.conf.urls.defaults import *
#from django.conf.urls import patterns, include, url
# from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib import auth

# from django.views.generic.list_detail import object_detail
from hitcount.views import update_hit_count_ajax
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView



admin.autodiscover()

urlpatterns = patterns('',
	url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Metten.blog.views.index', name='home'),
    url(r'^plots$', 'Metten.blog.views.plots', name='plots'),
    url(r'^graph$', 'Metten.blog.views.graph', name='graph'),
    url(r'^linker$', 'Metten.blog.views.linker', name='linker'),
    url(r'^blog/', include('Metten.blog.urls')),
    url(r'^5years/', include('Metten.years.urls'), name='5years_home')
)

urlpatterns += patterns('',


    # url(r'^login/$', 'login',  #this is django.contrib.auth.views.login
    #   {'template_name': 'login.html'},
    #   name='5years_login'),

    url(r'^login$', 'Metten.views.login'),
    url(r'^auth$', 'Metten.views.auth_view'),
    url(r'^logout$', 'Metten.views.logout'),
    url(r'^loggedin$', 'Metten.views.loggedin'),
    url(r'^invalid$', 'Metten.views.invalid_login'),
    url(r'^register$', 'Metten.views.register_user'),
    # url(r'^register_success$', 'Metten.views.register_success'),
	url(r'^survey$', TemplateView.as_view(template_name="survey.html")),
	url(r'^metten$', TemplateView.as_view(template_name="metten.html")),

    # 'django.contrib.auth.views',



    # url(r'^logout/$', 'logout',  #this is django.contrib.auth.views.logout
    #   {'next_page': '5years_home'},
    #   name='5years_logout'),


    # #static
    # (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #      {'document_root': settings.STATIC_ROOT}),

    # #media
    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #      {'document_root': settings.MEDIA_ROOT}),

	)


import debug_toolbar
urlpatterns += patterns('',
    url(r'^__debug__/', include(debug_toolbar.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()