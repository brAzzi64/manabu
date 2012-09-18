from django.conf.urls.defaults import patterns, include, url
import os

# calculated paths for the site used
# as starting points for other paths
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bun.views',

    url(r'^$', 'search'),
    url(r'^search$', 'search'),
    url(r'^train$', 'train'),
    url(r'^api/get_next_sentence$', 'get_next_sentence'),
    url(r'^api/learn_sentence$', 'learn_sentence'),
    url(r'^review$', 'review'),
    url(r'^known_kanji$', 'known_kanji'),
    url(r'^api/update_known_kanji$', 'update_known_kanji'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(APP_ROOT, 'static')}),
)

