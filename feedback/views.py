from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Walker, Wanderer
from .models import *
from accounts_auth.permissions import *
from fcm.send_notification import *
from asgiref.sync import async_to_sync


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWanderer])
def add_walker_feedback(request):
    
    wanderer = Wanderer.objects.filter(user=request.user).first()
    if not wanderer:
        return Response({"detail": "User is not a Wanderer"}, status=status.HTTP_403_FORBIDDEN)

    walker_id = request.data.get("walker_id")
    rating = request.data.get("rating")
    feedback = request.data.get("feedback", "")

    if not walker_id or not rating:
        return Response({"detail": "walker_id and rating are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        walker = Walker.objects.get(user=walker_id)
    except Walker.DoesNotExist:
        return Response({"detail": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)

    # Validate rating between 1 and 5
    rating = max(1, min(5, rating))

    old_rating = 0
    is_new_feedback = False

    try:
        feedback_obj = WalkerFeedback.objects.get(
            walker=walker, 
            wanderer=wanderer
        )
        # Existing feedback
        old_rating = feedback_obj.rating
        feedback_obj.rating = rating
        feedback_obj.feedback = feedback
        feedback_obj.save()
    except WalkerFeedback.DoesNotExist:
        # New feedback
        is_new_feedback = True
        feedback_obj = WalkerFeedback.objects.create(
            walker=walker,
            wanderer=wanderer,
            wanderer_name=wanderer.user.name,
            rating=rating,
            feedback=feedback
        )

    # Update walker rating stats
    walker.total_rating = walker.total_rating - old_rating + rating

    if is_new_feedback:
        walker.total_wanderer += 1  # increase count only for new feedback

    walker.save()
    title = "New Feedback Received"

    body = (
        f"{wanderer.user.name} rated you {rating}⭐"
        + (" and left feedback." if feedback else ".")
    )

    async_to_sync(sendNotifications)(
        user_id=walker.user.id,  
        title=title,
        body=body
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
        return Response({"detail": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

    if feedback.wanderer.user != request.user:
        return Response({"detail": "Not authorized to delete this feedback"}, status=status.HTTP_403_FORBIDDEN)

    feedback.delete()
    return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_walker_feedback(request, walker_id):
    try:
        walker = Walker.objects.get(user=walker_id)
    except Walker.DoesNotExist:
        return Response({"detail": "Walker not found"}, status=status.HTTP_404_NOT_FOUND)

    feedbacks = WalkerFeedback.objects.filter(walker=walker)
    data = [
        {
            "id": f.id,
            "wanderer_name": f.wanderer_name,
            "rating": f.rating,
            "feedback": f.feedback,
            "photo_url": f.wanderer.photo_url
        }
        for f in feedbacks
    ]
    return Response(data, status=status.HTTP_200_OK)


## Wanderer feedback
## walker will give feedback to wanderer
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsWalker])
def add_wanderer_feedback(request):
    
    walker = Walker.objects.filter(user=request.user).first()
    if not walker:
        return Response({"detail": "User is not a Walker"}, status=status.HTTP_403_FORBIDDEN)

    wanderer_id = request.data.get("wanderer_id")
    rating = request.data.get("rating")
    feedback = request.data.get("feedback")
    if not wanderer_id or not rating:
        return Response({"detail": "wanderer_id and rating are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        wanderer = Wanderer.objects.get(user=wanderer_id)
    except Wanderer.DoesNotExist:
        return Response({"detail": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)

    old_rating = 0
    repeated_user_feedback = WandererFeedback.objects.filter(walker = walker, wanderer = wanderer).first()
    new_feedback = False

    if repeated_user_feedback:
        old_rating = repeated_user_feedback.rating
        repeated_user_feedback.rating = rating 
        repeated_user_feedback.save()
    else :
        new_feedback = True
        wf = WandererFeedback.objects.create(
            walker=walker,
            wanderer=wanderer,
            walker_name=walker.user.name,
            rating=rating
        )

    new_total_rating = wanderer.total_rating - old_rating + rating
    new_total_walker = wanderer.total_walker
    if new_feedback:
        new_total_walker = new_total_walker + 1
    
    wanderer.total_rating = new_total_rating
    wanderer.total_walker = new_total_walker
    wanderer.save()
    title = "New Feedback Received"

    body = (
        f"{walker.user.name} rated you {rating}⭐"
        + (" and left feedback." if feedback else ".")
    )

    async_to_sync(sendNotifications)(
        user_id=walker.user.id,  
        title=title,
        body=body
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
        return Response({"detail": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

    if feedback.walker.user != request.user:
        return Response({"detail": "Not authorized to delete this feedback"}, status=status.HTTP_403_FORBIDDEN)

    feedback.delete()
    return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_wanderer_feedback(request, wanderer_id):
    try:
        wanderer = Wanderer.objects.get(user=wanderer_id)
    except Wanderer.DoesNotExist:
        return Response({"detail": "Wanderer not found"}, status=status.HTTP_404_NOT_FOUND)

    feedbacks = WandererFeedback.objects.filter(wanderer=wanderer)
    data = [
        {
            "id": f.id,
            "walker_name": f.walker_name,
            "rating": f.rating,
            "photo_url":f.walker.photo_url
        }
        for f in feedbacks
    ]
    return Response(data, status=status.HTTP_200_OK)
