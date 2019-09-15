from django.urls import re_path, path

from goodspost.views import *

urlpatterns = [

    path('', homeview.as_view()),
    re_path('^home/(?P<num>\d*)/$', homeview.as_view()),
    re_path('^category/(?P<num>\d*)/$', homeview.as_view()),
    re_path('^category/(?P<num>\d*)(\d*)$', homeview.as_view()),
    re_path('^goodsdetails/(?P<num>\d*)$', detailview.as_view())

]