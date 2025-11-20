from django.urls import path
from .views import *

urlpatterns = [
    path('users/update/', update_user_details, name='update_user_details'),
    path('users/update-role/', update_user_role, name='update_user_role'),
    path('update-walker/', update_walker_info, name='update_walker_info'),
    path('update-wanderer-preferences/',update_wanderer_preferences,name= 'update_wanderer_preferences'),
    path('update-user-profile/',update_user_profile,name = 'update_user_profile'),
    path('walker-info/<int:walker_id>/',get_walker_info,name='get_walker_info'),
    path('update-walker-status/',update_walker_status,name = 'update_walker_status'),
    path('get-walker-summary/',get_walker_summary,name='get_walker_summary'),
    path('get-wanderer-summary/',get_wanderer_summary,name = 'get_wanderer_summary'),
    path('get-wanderer-info/<int:wanderer_id>/',get_wanderer_info,name = 'get_wanderer_info'),
    path('get-wanderer-profile/',get_wanderer_profile,name='get_wanderer_profile'),
    path('get-walker-profile/',get_walker_profile,name='get_walker_profile')
]
