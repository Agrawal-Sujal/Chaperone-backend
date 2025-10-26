from django.urls import path
from .views import *

urlpatterns = [
    path('send/', send_request),
    path('reject/<int:request_id>/', reject_request),
    path('accept/<int:request_id>/', accept_request),
    path('withdraw/<int:request_id>/', withdraw_request),
    path('wanderer-requests/',get_all_wanderer_requests)
]
