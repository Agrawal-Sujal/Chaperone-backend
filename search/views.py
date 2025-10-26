from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts_auth.permissions import *
from django.utils import timezone
from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2
from accounts.models import *


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsWanderer])
def search_companion(request):
    try:
        user = request.user
        start_lat = float(request.data.get('start_lat'))
        start_long = float(request.data.get('start_long'))

        try:
            wanderer = Wanderer.objects.get(user=user)
        except Wanderer.DoesNotExist:
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        try:
            wanderer_preference = WandererPreferences.objects.get(wanderer=wanderer)
        except WandererPreferences.DoesNotExist:
            return Response({"error": "Preferences not found"}, status=status.HTTP_404_NOT_FOUND)

        language_preferences = WandererPreferenceLanguage.objects.filter(wanderer=wanderer_preference).values_list('language', flat=True)
        pace_preferences = WandererPreferenceWalkingPace.objects.filter(wanderer=wanderer_preference).values_list('walking_pace', flat=True)

        male = wanderer_preference.male
        female = wanderer_preference.female

        today = timezone.now().date()

        walkers = Walker.objects.filter(is_active=True, expiry_date__gte=today)

        matching_walkers = []

        for walker in walkers:
            if not walker.latitude or not walker.longitude:
                continue

            distance = calculate_distance(start_lat, start_long, walker.latitude, walker.longitude)
            if walker.max_walk_distance and distance > walker.max_walk_distance:
                continue  

            walker_gender = walker.male  
            if male is not walker_gender and female is not walker_gender:
                continue

            walker_languages = WalkerLanguage.objects.filter(walker=walker).values_list('language', flat=True)
            if not any(lang in walker_languages for lang in language_preferences):
                continue

            walker_paces = WalkerWalkingPace.objects.filter(walker=walker).values_list('walking_pace', flat=True)
            if not any(pace in walker_paces for pace in pace_preferences):
                continue

            rating = walker.total_rating/ walker.total_wanderer

            matching_walkers.append({
                "id": walker.user.id,
                "name": walker.name,
                "photo_url": walker.photo_url,
                "about": walker.about_yourself,
                "distance": distance,
                "rating": rating,
            })

        return Response({"results": matching_walkers}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_detail)

