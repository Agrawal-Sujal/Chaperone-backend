from django.urls import path
from .views import *

urlpatterns = [
    path('search_companion/', search_companion, name='search_companion')
]
