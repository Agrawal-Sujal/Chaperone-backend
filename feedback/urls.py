from django.urls import path
from .views import (
    add_walker_feedback, delete_walker_feedback, get_all_walker_feedback,
    add_wanderer_feedback, delete_wanderer_feedback, get_all_wanderer_feedback
)

urlpatterns = [
    # Walker feedback
    path('walker/add/', add_walker_feedback),
    path('walker/<int:feedback_id>/delete/', delete_walker_feedback),
    path('walker/<int:walker_id>/', get_all_walker_feedback),

    # Wanderer feedback
    path('wanderer/add/', add_wanderer_feedback),
    path('wanderer/<int:feedback_id>/delete/', delete_wanderer_feedback),
    path('wanderer/<int:wanderer_id>/', get_all_wanderer_feedback),
]
