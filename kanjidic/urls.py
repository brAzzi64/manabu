from django.conf.urls.defaults import patterns, include, url
import os

# calculated paths for the site used
# as starting points for other paths
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('kanjidic.views',

    url(r'^$', 'index'),
    #url(r'^(?P<kanji>.)/$', 'kanji'),
    url(r'^api/get_sentence_begin$', 'get_sentence_begin'),
    url(r'^api/get_sentence_next$', 'get_sentence_next'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(APP_ROOT, 'static')}),
)

