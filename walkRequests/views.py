from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Request
from accounts.models import Wanderer, Walker
from accounts_auth.permissions import *

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWanderer])
def send_request(request):
    try:
        wanderer = Wanderer.objects.get(user=request.user)
        walker_id = request.data.get("walker_id")

        if not walker_id:
            return Response({"detail": "walker_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # prevent duplicate pending requests
        if Request.objects.filter(
            wanderer=wanderer, walker_id=walker_id, is_accepted=False, is_rejected=False
        ).exists():
            return Response({"detail": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        req = Request.objects.create(
            wanderer=wanderer,
            walker_id=walker_id,
            date=request.data.get("date"),
            time=request.data.get("time"),
            loc_lat=request.data.get("loc_lat"),
            loc_long=request.data.get("loc_long"),
            location_name = request.data.get("location_name")
        )

        

        return Response({'message':"Request send successfully."}, status=status.HTTP_201_CREATED)

    except Wanderer.DoesNotExist:
        return Response({"detail": "Only wanderers can send requests"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWalker])
def reject_request(request):
    try:
        walker = Walker.objects.get(user=request.user)
        request_id = request.data.get('request_id')
        req = Request.objects.get(id=request_id, walker=walker)

        if req.is_accepted:
            return Response({"detail": "Request already accepted"}, status=status.HTTP_400_BAD_REQUEST)
        if req.is_rejected:
            return Response({"detail": "Request already rejected"}, status=status.HTTP_400_BAD_REQUEST)


        req.is_rejected = True
        req.rejection_reason = request.data.get("rejection_reason", "")
        req.save()

        return Response({
            "message": "Request rejected successfully",
            "id": req.id,
            "rejection_reason": req.rejection_reason
        })

    except Walker.DoesNotExist:
        return Response({"detail": "Only walkers can reject requests"}, status=status.HTTP_403_FORBIDDEN)
    except Request.DoesNotExist:
        return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWalker])
def accept_request(request):
    try:
        walker = Walker.objects.get(user=request.user)
        request_id = request.data.get('request_id')
        req = Request.objects.get(id=request_id, walker=walker)

        if req.is_rejected:
            return Response({"detail": "Request already rejected"}, status=status.HTTP_400_BAD_REQUEST)
        if req.is_accepted:
            return Response({"detail": "Request already accepted"}, status=status.HTTP_400_BAD_REQUEST)

        req.is_accepted = True
        req.save()

        return Response({
            "message": "Request accepted successfully",
            "id": req.id,
            "is_accepted": req.is_accepted
        })

    except Walker.DoesNotExist:
        return Response({"detail": "Only walkers can accept requests"}, status=status.HTTP_403_FORBIDDEN)
    except Request.DoesNotExist:
        return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsWanderer])
def withdraw_request(request, request_id):
    try:
        wanderer = Wanderer.objects.get(user=request.user)
        req = Request.objects.get(id=request_id, wanderer=wanderer)

        if req.is_accepted:
            return Response({"detail": "Cannot withdraw an accepted request"}, status=status.HTTP_400_BAD_REQUEST)

        req.delete()
        return Response({"message": "Request withdrawn successfully"})

    except Wanderer.DoesNotExist:
        return Response({"detail": "Only wanderers can withdraw requests"}, status=status.HTTP_403_FORBIDDEN)
    except Request.DoesNotExist:
        return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_wanderer_requests(request):
    try:
        wanderer = Wanderer.objects.get(user=request.user)
        requests_qs = Request.objects.filter(wanderer=wanderer).order_by('-created_at')

        data = []
        for r in requests_qs:
            data.append({
                "id": r.id,
                "walker_id": r.walker.user.id,
                "walker_name": r.walker.name if hasattr(r.walker, 'name') else None,
                "is_accepted": r.is_accepted,
                "is_rejected": r.is_rejected,
                "rejection_reason": r.rejection_reason,
                "date": str(r.date),
                "location_name": r.location_name,
                "time": r.time,
                "loc_lat": r.loc_lat,
                "loc_long": r.loc_long,
                "fees_paid": r.fees_paid,
                "payment_id": r.payment_id,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return Response(data, status=status.HTTP_200_OK)

    except Wanderer.DoesNotExist:
        return Response({"error": "Only wanderers can view their requests"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_walker_requests(request):
    try:
        walker = Walker.objects.get(user=request.user)
        # Get only pending requests (not accepted & not rejected)
        requests_qs = Request.objects.filter(
            walker=walker,
            is_accepted=False,
            is_rejected=False
        ).order_by('-created_at')
        
        data = []
        for r in requests_qs:
            if r.wanderer.total_walker is not 0:
                rating = r.wanderer.total_rating / r.wanderer.total_walker
            else : rating = 0
            distance = calculate_distance(r.loc_lat,r.loc_long,walker.latitude,walker.longitude)
            data.append({
                "id": r.id,
                "wanderer_id": r.wanderer.user.id,
                "wanderer_name": r.wanderer.name if hasattr(r.wanderer, 'name') else None,
                "wanderer_rating": rating,
                "date": str(r.date),
                "location_name": r.location_name,
                "time": r.time,
                "loc_lat": r.loc_lat,
                "loc_long": r.loc_long,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "distance": distance
            })

        return Response(data, status=status.HTTP_200_OK)

    except Walker.DoesNotExist:
        return Response({"error": "Only walkers can view pending requests"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)