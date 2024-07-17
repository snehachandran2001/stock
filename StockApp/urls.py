# stockdata/urls.py
from django.urls import path
from .views import get_auth_url, handle_redirect, fetch_live_data

urlpatterns = [
    path('auth/', get_auth_url, name='get_auth_url'),
    path('redirect/', handle_redirect, name='handle_redirect'),
    path('fetch/', fetch_live_data, name='fetch_live_data'),
]
