from django.urls import path

from userapp.views import *

urlpatterns = [
    path('user/register/', Register.as_view()),
    path('user/check/', judge),
    path('user/center/', Center.as_view(), name='center'),
    path('user/login/', Login.as_view(), name='login'),
    path('user/loadcode/', Loadcode.as_view()),
    path('user/checkcode/', checkcode),
    path('user/logout/', logout),
    path('user/address/', Address_view.as_view(), name='addr'),
    path("user/address/reload/", change_area),
]