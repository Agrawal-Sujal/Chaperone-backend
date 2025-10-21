from django.urls import path
from .views import register_view, login_view, google_auth_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('google-auth/', google_auth_view, name='google-auth'),
]
