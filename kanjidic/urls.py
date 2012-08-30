from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('kanjidic.views',

    url(r'^$', 'index'),
    url(r'^(?P<kanji>.)/$', 'kanji'),
    url(r'^get_sentence_begin$', 'get_sentence_begin'),
    url(r'^get_sentence_next$', 'get_sentence_next'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
