from django.urls import path
from .views import *

urlpatterns = [
    path('users/update/', update_user_details, name='update_user_details'),
    path('users/update-role/', update_user_role, name='update_user_role'),
    path('update-walker/', update_walker_info, name='update_walker_info'),
    path('update-wanderer-preferences/',update_wanderer_preferences,name= 'update_wanderer_preferences')
]
