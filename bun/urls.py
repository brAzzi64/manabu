import os
from django.conf.urls.defaults import patterns, include, url

# calculated paths for the site used
# as starting points for other paths
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

urlpatterns = patterns('bun.views.train',

    url(r'^$', 'train'),
    url(r'^train$', 'train'),
    url(r'^train/api/get_sentences$', 'get_sentences'),
    url(r'^train/api/learn_sentence$', 'learn_sentence'),
)

urlpatterns += patterns('bun.views.known_kanji',

    url(r'^known_kanji$', 'known_kanji'),
    url(r'^known_kanji/api/update_known_kanji$', 'update_known_kanji'),
)

urlpatterns += patterns('bun.views.review',

    url(r'^review$', 'review'),
)

urlpatterns += patterns('',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(APP_ROOT, 'static')}),
)

