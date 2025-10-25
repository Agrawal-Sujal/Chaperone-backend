from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from accounts_auth.permissions import *
from django.utils import timezone
from datetime import timedelta

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_details(request):
    try:
        user = request.user 

        name = request.data.get('name')
        date_of_birth = request.data.get('date_of_birth')
        phone_number = request.data.get('phone_number')

        user.name = name
        user.date_of_birth = date_of_birth
        user.phone_number = phone_number

        user.save()
        return Response({
            'message': 'User details updated successfully',
            # 'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "detail": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_detail)

    


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_role(request):
    try:
        user = request.user
        is_walker = request.data.get("is_walker")

        if isinstance(is_walker, str):
            is_walker = is_walker.lower() == "true"

        user.is_walker = is_walker
        user.save()

        if is_walker:
            Wanderer.objects.filter(user=user).delete()

            walker, created = Walker.objects.get_or_create(user=user,name = user.name,defaults=[{"expiry_date":  timezone.now() + timedelta(days=7)}])
            message = "User promoted to Walker." if created else "User role updated to Walker."
        else:
            Walker.objects.filter(user=user).delete()

            wanderer, created = Wanderer.objects.get_or_create(user=user,name = user.name)
            message = "User promoted to Wanderer." if created else "User role updated to Wanderer."

        return Response({
            "message": message,
            # "user_id": user.id,
            # "is_walker": user.is_walker
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "detail": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_detail)





@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated,IsWanderer])
def update_wanderer_preferences(request):

    try:
        user = request.user

        # Ensure the user is a Wanderer
        try:
            wanderer = Wanderer.objects.get(user=user)
        except Wanderer.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        need_mobility_assistance = request.data.get("need_mobility_assistance", False)
        walking_pace_ids = request.data.get("walking_pace_ids", [])
        language_ids = request.data.get("language_ids", [])
        charity_ids = request.data.get("charity_ids", [])
        male = request.data.get("male")
        female = request.data.get("female")

        preferences, created = WandererPreferences.objects.get_or_create(
            wanderer = wanderer, 
            defaults = {"need_mobility_assistance": need_mobility_assistance,"male":male,"female":female}
        )

        if not created:
            preferences.need_mobility_assistance = need_mobility_assistance
            preferences.male = male
            preferences.female = female
            preferences.save()

        if walking_pace_ids:
            WandererPreferenceWalkingPace.objects.filter(wanderer=preferences).delete()  # When you do filter(wanderer=preferences), Django automatically uses the primary key (id) of the preferences object under the hood.
            for pace_id in walking_pace_ids:
                try:
                    pace = WalkingPace.objects.get(id=pace_id)
                    WandererPreferenceWalkingPace.objects.create(wanderer=preferences, walking_pace=pace)
                except WalkingPace.DoesNotExist:
                    continue

        if language_ids:
            WandererPreferenceLanguage.objects.filter(wanderer=preferences).delete()
            for lang_id in language_ids:
                try:
                    lang = Language.objects.get(id=lang_id)
                    WandererPreferenceLanguage.objects.create(wanderer=preferences, language=lang)
                except Language.DoesNotExist:
                    continue

        if charity_ids:
            WandererPreferenceCharity.objects.filter(wanderer=preferences).delete()
            for charity_id in charity_ids:
                try:
                    charity = Charity.objects.get(id=charity_id)
                    WandererPreferenceCharity.objects.create(wanderer=preferences, charity=charity)
                except Charity.DoesNotExist:
                    continue

        return Response({
            "message": "Preferences updated successfully.",
            # "need_mobility_assistance": preferences.need_mobility_assistance,
            # "walking_pace_ids": walking_pace_ids,
            # "language_ids": language_ids,
            # "charity_ids": charity_ids
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "detail": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_detail)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated,IsWalker])
def update_walker_info(request):
    try:
        user = request.user
        # Ensure the user is a Walker
        try:
            walker = Walker.objects.get(user=user)
        except Walker.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Update basic info
        walker.photo_url = request.data.get('photo_url', walker.photo_url)
        walker.about_yourself = request.data.get('about_yourself', walker.about_yourself)
        walker.male = request.data.get('male',walker.male)
        walker.save()

        language_ids = request.data.get('language_ids')
        if language_ids is not None:
            # Remove old ones
            WalkerLanguage.objects.filter(walker=walker).delete()
            # Add new ones
            for lang_id in language_ids:
                lang = Language.objects.get(id=lang_id)
                WalkerLanguage.objects.create(walker=walker, language=lang)

        walking_pace_ids = request.data.get('walking_pace_ids')
        if walking_pace_ids is not None:
            WalkerWalkingPace.objects.filter(walker=walker).delete()
            for pace_id in walking_pace_ids:
                pace = WalkingPace.objects.get(id=pace_id)
                WalkerWalkingPace.objects.create(walker=walker, walking_pace=pace)

        return Response({ "message": "Walker info updated successfully."},status= status.HTTP_200_OK)

    except Exception as e:
        return Response({ "detail": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_detail)