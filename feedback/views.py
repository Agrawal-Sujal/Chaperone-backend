from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Walker, Wanderer
from .models import *
from accounts_auth.permissions import *


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWanderer])
def add_walker_feedback(request):
    
    wanderer = Wanderer.objects.filter(user=request.user).first()
    if not wanderer:
        return Response({"error": "User is not a Wanderer"}, status=status.HTTP_403_FORBIDDEN)

    walker_id = request.data.get("walker_id")
    rating = request.data.get("rating")
    feedback = request.data.get("feedback", "")

    if not walker_id or not rating:
        return Response({"error": "walker_id and rating are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        walker = Walker.objects.get(user=walker_id)
    except Walker.DoesNotExist:
        return Response({"error": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)

    wf = WalkerFeedback.objects.create(
        walker=walker,
        wanderer=wanderer,
        wanderer_name=wanderer.user.name,
        rating=rating,
        feedback=feedback
    )

    return Response({
        "message": "Feedback submitted successfully"
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsWanderer])
def delete_walker_feedback(request, feedback_id):
    try:
        feedback = WalkerFeedback.objects.get(id=feedback_id)
    except WalkerFeedback.DoesNotExist:
        return Response({"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

    if feedback.wanderer.user != request.user:
        return Response({"error": "Not authorized to delete this feedback"}, status=status.HTTP_403_FORBIDDEN)

    feedback.delete()
    return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_walker_feedback(request, walker_id):
    try:
        walker = Walker.objects.get(user=walker_id)
    except Walker.DoesNotExist:
        return Response({"error": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)

    feedbacks = WalkerFeedback.objects.filter(walker=walker)
    data = [
        {
            "id": f.id,
            "wanderer_name": f.wanderer_name,
            "rating": f.rating,
            "feedback": f.feedback,
        }
        for f in feedbacks
    ]
    return Response(data, status=status.HTTP_200_OK)


## Wanderer feedback

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWalker])
def add_wanderer_feedback(request):
    
    walker = Walker.objects.filter(user=request.user).first()
    if not walker:
        return Response({"error": "User is not a Walker"}, status=status.HTTP_403_FORBIDDEN)

    wanderer_id = request.data.get("wanderer_id")
    rating = request.data.get("rating")

    if not wanderer_id or not rating:
        return Response({"error": "wanderer_id and rating are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        wanderer = Wanderer.objects.get(user=wanderer_id)
    except Wanderer.DoesNotExist:
        return Response({"error": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)

    wf = WandererFeedback.objects.create(
        walker=walker,
        wanderer=wanderer,
        walker_name=walker.user.name,
        rating=rating
    )

    return Response({
        "message": "Feedback submitted successfully"
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsWalker])
def delete_wanderer_feedback(request, feedback_id):
    try:
        feedback = WandererFeedback.objects.get(id=feedback_id)
    except WandererFeedback.DoesNotExist:
        return Response({"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

    if feedback.walker.user != request.user:
        return Response({"error": "Not authorized to delete this feedback"}, status=status.HTTP_403_FORBIDDEN)

    feedback.delete()
    return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_wanderer_feedback(request, wanderer_id):
    try:
        wanderer = Wanderer.objects.get(user=wanderer_id)
    except Wanderer.DoesNotExist:
        return Response({"error": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)

    feedbacks = WandererFeedback.objects.filter(wanderer=wanderer)
    data = [
        {
            "id": f.id,
            "walker_name": f.walker_name,
            "rating": f.rating
        }
        for f in feedbacks
    ]
    return Response(data, status=status.HTTP_200_OK)
