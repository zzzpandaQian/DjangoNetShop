from django.urls import path

from cartapp.views import *
urlpatterns = [
    path('cart/', Cartview.as_view()),
    path('cart/prepay/', Cartview.as_view(), name='prepay'),
]