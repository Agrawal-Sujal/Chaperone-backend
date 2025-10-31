from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from accounts_auth.permissions import *
from django.utils import timezone
from datetime import timedelta
from feedback.models import *

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
        user.is_verified = True
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
        try:
            walker = Walker.objects.get(user=user)
        except Walker.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        walker.photo_url = request.data.get('photo_url', walker.photo_url)
        walker.about_yourself = request.data.get('about_yourself', walker.about_yourself)
        walker.male = request.data.get('male',walker.male)
        walker.save()

        language_ids = request.data.get('language_ids')
        if language_ids is not None:
            WalkerLanguage.objects.filter(walker=walker).delete()
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
    


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        user = request.user
        is_walker = request.data.get("is_walker")

        if isinstance(is_walker, str):
            is_walker = is_walker.lower() == "true"

        photo_url = request.data.get("photo_url")
        about_yourself = request.data.get("about_yourself")
        male = request.data.get("male")
        female = request.data.get("female")
        need_mobility_assistance = request.data.get("need_mobility_assistance", False)

        walking_pace_ids = request.data.get("walking_pace_ids", [])
        language_ids = request.data.get("language_ids", [])
        charity_ids = request.data.get("charity_ids", [])

        

        Walker.objects.filter(user=user).delete()
        Wanderer.objects.filter(user=user).delete()

        if is_walker:
            walker, _ = Walker.objects.get_or_create(
                user=user,
                defaults={
                    "name": user.name,
                    "expiry_date": timezone.now() + timedelta(days=7),
                    "photo_url": photo_url,
                    "about_yourself": about_yourself,
                    "male": male
                }
            )

            walker.photo_url = photo_url or walker.photo_url
            walker.about_yourself = about_yourself or walker.about_yourself
            walker.male = male if male is not None else walker.male
            walker.save()

            WalkerLanguage.objects.filter(walker=walker).delete()
            for lang_id in language_ids:
                try:
                    lang = Language.objects.get(id=lang_id+1)
                    WalkerLanguage.objects.create(walker=walker, language=lang)
                except Language.DoesNotExist:
                    continue

            WalkerWalkingPace.objects.filter(walker=walker).delete()
            for pace_id in walking_pace_ids:
                try:
                    pace = WalkingPace.objects.get(id=pace_id+1)
                    WalkerWalkingPace.objects.create(walker=walker, walking_pace=pace)
                except WalkingPace.DoesNotExist:
                    continue

            message = "Walker details saved successfully."
            user.is_walker = is_walker
            user.is_profile_completed = True
            user.save()

        else:
            wanderer, _ = Wanderer.objects.get_or_create(user=user, name=user.name)

            preferences, _ = WandererPreferences.objects.get_or_create(
                wanderer=wanderer,
                defaults={
                    "need_mobility_assistance": need_mobility_assistance,
                    "male": male,
                    "female": female
                }
            )

            preferences.need_mobility_assistance = need_mobility_assistance
            preferences.male = male
            preferences.female = female
            preferences.save()

            WandererPreferenceWalkingPace.objects.filter(wanderer=preferences).delete()
            for pace_id in walking_pace_ids:
                try:
                    pace = WalkingPace.objects.get(id=pace_id+1)
                    WandererPreferenceWalkingPace.objects.create(wanderer=preferences, walking_pace=pace)
                except WalkingPace.DoesNotExist:
                    continue

            WandererPreferenceLanguage.objects.filter(wanderer=preferences).delete()
            for lang_id in language_ids:
                try:
                    lang = Language.objects.get(id=lang_id+1)
                    WandererPreferenceLanguage.objects.create(wanderer=preferences, language=lang)
                except Language.DoesNotExist:
                    continue

            WandererPreferenceCharity.objects.filter(wanderer=preferences).delete()
            for charity_id in charity_ids:
                try:
                    charity = Charity.objects.get(id=charity_id+1)
                    WandererPreferenceCharity.objects.create(wanderer=preferences, charity=charity)
                except Charity.DoesNotExist:
                    continue

            message = "Wanderer details saved successfully."
            user.is_walker = is_walker
            user.is_profile_completed = True
            user.save()
            
        return Response({"message": message}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_walker_info(request, walker_id):
    try:
        # Get the walker object
        walker = Walker.objects.get(user_id=walker_id)
        
        # Get walker's walking paces
        walker_paces = WalkerWalkingPace.objects.filter(walker=walker).select_related('walking_pace')
        paces = [wp.walking_pace.name for wp in walker_paces]
        
        # Get walker's languages
        walker_languages = WalkerLanguage.objects.filter(walker=walker).select_related('language')
        languages = [wl.language.name for wl in walker_languages]
        
        # Get wanderer feedbacks for this walker
        feedbacks = WalkerFeedback.objects.filter(walker=walker).values(
            'wanderer_name', 
            'rating', 
            'feedback'
        )
        
        # Calculate average rating
        if walker.total_wanderer > 0:
            average_rating = walker.total_rating / walker.total_wanderer
        else:
            average_rating = 0
        
        # Prepare response data
        walker_data = {
            'name': walker.name,
            'rating': round(average_rating, 2),
            'about': walker.about_yourself,
            'paces': paces,
            'languages': languages,
            'feedbacks': list(feedbacks)
        }
        
        return Response(walker_data, status=status.HTTP_200_OK)
        
    except Walker.DoesNotExist:
        return Response({"detail": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wanderer_info(request, wanderer_id):
    try:
        # Get the walker object
        wanderer = Wanderer.objects.get(user_id=wanderer_id)
        wanderer_pref = WandererPreferences.objects.get(wanderer = wanderer)
        # Get walker's walking paces
        wanderer_paces = WandererPreferenceWalkingPace.objects.filter(wanderer = wanderer_pref).select_related('walking_pace')
        paces = [wp.walking_pace.name for wp in wanderer_paces]
        
        # Get walker's languages
        wanderer_language = WandererPreferenceLanguage.objects.filter(wanderer = wanderer_pref).select_related('language')
        languages = [wl.language.name for wl in wanderer_language]

        
        # Calculate average rating
        if wanderer.total_walker > 0:
            average_rating = wanderer.total_rating / wanderer.total_walker
        else:
            average_rating = 0
        
        # Prepare response data
        wanderer_data = {
            'name': wanderer.name,
            'rating': round(average_rating, 2),
            'paces': paces,
            'languages': languages,
        }
        
        return Response(wanderer_data, status=status.HTTP_200_OK)
        
    except Wanderer.DoesNotExist:
        return Response({"detail": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsWanderer])
def get_wanderer_summary(request):
    try:
        user = request.user
        try:
            wanderer = Wanderer.objects.get(user=user)
        except Wanderer.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        if wanderer.total_walker is not 0:
            rating = wanderer.total_rating / wanderer.total_walker
        else : rating = 0
        wanderer_summary = {
            "total_charity": wanderer.total_charity,
            "total_walks": wanderer.total_walks,
            "rating": rating
        }
        return Response(wanderer_summary,status = status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsWalker])
def get_walker_summary(request):
    try:
        user = request.user
        try:
            walker = Walker.objects.get(user=user)
        except Walker.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        if walker.total_wanderer is not 0:
            rating = walker.total_rating / walker.total_wanderer
        else : rating = 0
        walker_summary = {
            "total_earning": walker.total_earning,
            "total_walks": walker.total_walks,
            "rating": rating,
            "is_active": walker.is_active,
            "max_distance": walker.max_walk_distance,
            "location_name": walker.location_name,
            "long":walker.longitude,
            "lat":walker.latitude
        }
        return Response(walker_summary,status = status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsWalker])
def update_walker_status(request):
    try:
        user = request.user
        is_active = request.data.get('is_active')
        max_distance = request.data.get('max_distance')
        location_name = request.data.get('location_name')
        long = request.data.get('long')
        lat = request.data.get('lat')
        print(long)
        print(lat)
        try:
            walker = Walker.objects.get(user=user)
        except Walker.DoesNotExist:
            return Response({"detail": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        walker.is_active = is_active
        walker.max_walk_distance = max_distance
        walker.location_name = location_name
        walker.longitude = long
        walker.latitude = lat
        walker.save()
        message = "Status updated successfully"
        return Response({"message": message}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    