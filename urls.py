# coding=utf-8

import os

import settings

from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, 'admin-media')}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^zrender/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.STATIC_ROOT, 'echarts', 'zrender')}),
    (r'^admin/', include(admin.site.urls)),

    (r'^kchart/', 'fundc.web.kchart.views.kchart'),
    (r'^$', 'fundc.web.main.views.index'),
)

handler404 = 'fundc.web.main.views.page_not_found'
handler500 = 'fundc.web.main.views.page_error'
