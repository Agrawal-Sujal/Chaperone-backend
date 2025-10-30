from django.urls import path
from .views import *

urlpatterns = [
    path('send/', send_request),
    path('reject/', reject_request),
    path('accept/', accept_request),
    path('withdraw/<int:request_id>/', withdraw_request),
    path('wanderer-requests/',get_all_wanderer_requests),
    path('get-pending-walker-requests/',get_pending_walker_requests,name='get_pending_walker_requests')
]
