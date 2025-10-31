from django.urls import path
from .views import *

urlpatterns = [
    path("room/<int:room_id>/", get_room_info, name="get_room_info"),
    path("wanderer/scheduled-walks/", get_wanderer_scheduled_walks, name="wanderer_scheduled_walks"),
    path("walker/scheduled-walks/", get_walker_scheduled_walks, name="walker_scheduled_walks"),
    path("complete-walk/<int:room_id>/", complete_walk, name="complete_walk"),
    path("wanderer/completed-walks/", get_completed_wanderer_walks, name="wanderer_completed_walks"),
    path("walker/completed-walks/", get_completed_walker_walks, name="walker_completed_walks"),
]
