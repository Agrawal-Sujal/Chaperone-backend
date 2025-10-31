from django.urls import re_path
from walks import consumers

websocket_urlpatterns = [
    re_path(r'ws/location/(?P<room_name>\w+)/$', consumers.LocationChannel.as_asgi()),
]
