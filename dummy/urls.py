from django.conf.urls import patterns, include, url
from search.models import WebSite
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url('^index/$', ListView.as_view(
    #        queryset=WebSite.objects.all(),
    #        context_object_name='site_list',
    #        template_name='search/index.html')),
    url(r'^search_results/$', 'search.views.search_results', name='search_result'),
    url(r'^website/(?P<website_id>\d+)/$$', 'search.views.website', name='website'),
    url(r'^search/$', 'search.views.search', name='search'),
    url(r'^advanced_search/$', 'search.views.advanced_search', name='advanced_search'),
    # url(r'^dummy/', include('dummy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^prova/', 'search.views.prova', name='prova'),
    url(r'^admin/', include(admin.site.urls)),
)
