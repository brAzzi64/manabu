import os
from django.conf.urls.defaults import patterns, include, url

# calculated paths for the site used
# as starting points for other paths
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

urlpatterns = patterns('bun.views.train',

    url(r'^train$', 'train'),
    url(r'^train/api/get_sentences$', 'get_sentences'),
    url(r'^train/api/learn_sentence$', 'learn_sentence'),
    url(r'^train/api/get_audio$', 'get_audio'),
)

urlpatterns += patterns('bun.views.known_kanji',

    url(r'^known_kanji$', 'known_kanji'),
    url(r'^known_kanji/api/get_kanji$', 'get_kanji'),
    url(r'^known_kanji/api/update_known_kanji$', 'update_known_kanji'),
)

urlpatterns += patterns('bun.views.history',

    url(r'^history$', 'history'),
    url(r'^history/api/get_sentences$', 'get_sentences'),
)

urlpatterns += patterns('bun.views.review',

    url(r'^review$', 'review'),
    url(r'^review/api/get_random_sentence$', 'get_random_sentence'),
)

urlpatterns += patterns('bun.views.authentication',

    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^$', 'start'), # /bun
)

urlpatterns += patterns('bun.views.maintenance',

    url(r'^maintenance/exportdata$', 'exportdata'),
    url(r'^maintenance/importdata$', 'importdata'),
)

urlpatterns += patterns('',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(APP_ROOT, 'static')}),
)

