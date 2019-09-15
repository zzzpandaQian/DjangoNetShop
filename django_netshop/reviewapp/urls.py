from django.urls import path
from reviewapp.views import *
urlpatterns = [
    path('order/', Orderview.as_view(), name='orederhome'),
    path('orderlogin/', orderlogin),
    path('order/toorder/', toorder),
    path('order/checkpay/', checkpay),
]