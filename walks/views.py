from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Room, ScheduledWalks
from accounts.models import Walker, Wanderer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_room_info(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        data = {
            "id": room.id,
            "walker_id": room.walker.user.id,
            "wanderer_id": room.wanderer.user.id,
            "wanderer_name": room.wanderer.name,
            "walker_name": room.walker.name,
            "start_location_name": room.start_location_name,
            "start_location_latitude": room.start_location_latitude,
            "start_location_longitude": room.start_location_longitude,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wanderer_scheduled_walks(request):
    try:
        wanderer = Wanderer.objects.get(user=request.user)
        walks = ScheduledWalks.objects.filter(wanderer=wanderer, walk_completed=False)

        print(wanderer)
        print(walks)

        data = []
        for walk in walks:
            if walk.wanderer.total_walker == 0:
                wanderer_rating = 0
            else : 
                wanderer_rating = walk.wanderer.total_rating / walk.wanderer.total_walker

            if walk.walker.total_wanderer == 0:
                walker_rating = 0
            else : 
                walker_rating = walk.walker.total_rating / walk.walker.total_wanderer
            data.append({
                "id": walk.id,
                "walker_id": walk.walker.user.id,
                "wanderer_id": walk.wanderer.user.id,
                "room_id": walk.room.id,
                "date": walk.date,
                "time":walk.time,
                "start_location_name": walk.start_location_name,
                "start_location_latitude": walk.start_location_latitude,
                "start_location_longitude": walk.start_location_longitude,
                "walker_name": walk.walker.name,
                "wanderer_name": walk.wanderer.name,
                "walker_profile_url":walk.walker.photo_url,
                "wanderer_rating":wanderer_rating,
                "walker_rating": walker_rating
            })

        print(data)
        return Response(data, status=status.HTTP_200_OK)
    except Wanderer.DoesNotExist:
        return Response({"detail": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_walker_scheduled_walks(request):
    try:
        walker = Walker.objects.get(user=request.user)
        walks = ScheduledWalks.objects.filter(walker=walker, walk_completed=False)

        data = []
        for walk in walks:
            if walk.wanderer.total_walker == 0:
                wanderer_rating = 0
            else : 
                wanderer_rating = walk.wanderer.total_rating / walk.wanderer.total_walker

            if walk.walker.total_wanderer == 0:
                walker_rating = 0
            else : 
                walker_rating = walk.walker.total_rating / walk.walker.total_wanderer
            data.append({
                "id": walk.id,
                "walker_id": walk.walker.user.id,
                "wanderer_id": walk.wanderer.user.id,
                "room_id": walk.room.id,
                "date": walk.date,
                "time":walk.time,
                "start_location_name": walk.start_location_name,
                "start_location_latitude": walk.start_location_latitude,
                "start_location_longitude": walk.start_location_longitude,
                "walker_name": walk.walker.name,
                "wanderer_name": walk.wanderer.name,
                "walker_profile_url":walk.walker.photo_url,
                "wanderer_rating":wanderer_rating,
                "walker_rating": walker_rating
            })
        return Response(data, status=status.HTTP_200_OK)
    except Walker.DoesNotExist:
        return Response({"detail": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_walk(request, room_id):
    try:
        walk = ScheduledWalks.objects.get(room__id=room_id)
        walk.walk_completed = True
        walk.walker.total_walks +=1
        walk.wanderer.total_walks +=1
        walk.wanderer.save()
        walk.walker.save()
        
        walk.save()
        return Response({"message": "Walk marked as completed"}, status=status.HTTP_200_OK)
    except ScheduledWalks.DoesNotExist:
        return Response({"detail": "Scheduled walk not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_wanderer_walks(request):
    try:
        wanderer = Wanderer.objects.get(user=request.user)
        walks = ScheduledWalks.objects.filter(wanderer=wanderer, walk_completed=True)

        data = []
        for walk in walks:
            if walk.wanderer.total_walker == 0:
                wanderer_rating = 0
            else : 
                wanderer_rating = walk.wanderer.total_rating / walk.wanderer.total_walker

            if walk.walker.total_wanderer == 0:
                walker_rating = 0
            else : 
                walker_rating = walk.walker.total_rating / walk.walker.total_wanderer
            data.append({
                "id": walk.id,
                "walker_id": walk.walker.user.id,
                "wanderer_id": walk.wanderer.user.id,
                "room_id": walk.room.id,
                "date": walk.date,
                "time":walk.time,
                "start_location_name": walk.start_location_name,
                "start_location_latitude": walk.start_location_latitude,
                "start_location_longitude": walk.start_location_longitude,
                "walker_name": walk.walker.name,
                "wanderer_name": walk.wanderer.name,
                "walker_profile_url":walk.walker.photo_url,
                "wanderer_rating":wanderer_rating,
                "walker_rating": walker_rating
            })
        return Response(data, status=status.HTTP_200_OK)
    except Wanderer.DoesNotExist:
        return Response({"detail": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_walker_walks(request):
    try:
        walker = Walker.objects.get(user=request.user)
        walks = ScheduledWalks.objects.filter(walker=walker, walk_completed=True)

        data = []
        for walk in walks:
            if walk.wanderer.total_walker == 0:
                wanderer_rating = 0
            else : 
                wanderer_rating = walk.wanderer.total_rating / walk.wanderer.total_walker

            if walk.walker.total_wanderer == 0:
                walker_rating = 0
            else : 
                walker_rating = walk.walker.total_rating / walk.walker.total_wanderer
            data.append({
                "id": walk.id,
                "walker_id": walk.walker.user.id,
                "wanderer_id": walk.wanderer.user.id,
                "room_id": walk.room.id,
                "date": walk.date,
                "time":walk.time,
                "start_location_name": walk.start_location_name,
                "start_location_latitude": walk.start_location_latitude,
                "start_location_longitude": walk.start_location_longitude,
                "walker_name": walk.walker.name,
                "wanderer_name": walk.wanderer.name,
                "walker_profile_url":walk.walker.photo_url,
                "wanderer_rating":wanderer_rating,
                "walker_rating": walker_rating
            })
        return Response(data, status=status.HTTP_200_OK)
    except Walker.DoesNotExist:
        return Response({"detail": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
