import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import PaymentOrder
import traceback
import hmac
import hashlib
from walkRequests.models import *
from walks.models import *
from asgiref.sync import async_to_sync
from fcm.send_notification import sendNotifications




class CreateOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            request_id = request.data.get('request_id')
            amount = request.data.get("amount")  
            currency = request.data.get("currency", "INR")

            if not amount:
                return Response({"detail": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                request = Request.objects.get(id=request_id)
            except Request.DoesNotExist:
                return Response({"detail": "Request not found"}, status=status.HTTP_403_FORBIDDEN)
            
            if request.fees_paid:
                return Response({"detail":"You already paid the fees"},status=status.HTTP_403_FORBIDDEN)

            amount_in_paise = int(float(amount) * 100)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            order_data = {
                "amount": amount_in_paise,
                "currency": currency,
                "receipt": "receipt#1",
                "payment_capture": 1
            }
            order = client.order.create(data=order_data)

            # ✅ Save order in database
            payment = PaymentOrder.objects.create(
                order_id=order["id"],
                amount=amount_in_paise,
                currency=currency,
                status="created"
            )

            request.payment_id = payment.id
            request.save()

            return Response({
                "id":payment.id,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key": settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VerifyOrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            id = request.data.get('id')
            razorpay_payment_id = request.data.get("payment_id")
            razorpay_order_id = request.data.get("order_id")
            razorpay_signature = request.data.get("signature")

            if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
                return Response({"detail": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                request = Request.objects.get(payment_id=id)
            except Request.DoesNotExist:
                return Response({"detail": "Request not found"}, status=status.HTTP_403_FORBIDDEN)
            
            

            # Generate expected signature
            msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                msg,
                hashlib.sha256
            ).hexdigest()

             # Verify
            if not hmac.compare_digest(generated_signature, razorpay_signature):
                order = PaymentOrder.objects.get(order_id=razorpay_order_id)
                order.payment_id = razorpay_payment_id
                order.signature = razorpay_signature
                order.status = "failed"
                order.save()
                return Response({"detail": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

           

            # ✅ Create Room
            room = Room(
                walker=request.walker,
                wanderer=request.wanderer,
                start_location_name=request.location_name,
                start_location_latitude=request.loc_lat,
                start_location_longitude=request.loc_long
            )

            room.save()

            # ✅ Create ScheduledWalks
            scheduled_walk = ScheduledWalks.objects.create(
                walker=request.walker,
                wanderer=request.wanderer,
                room=room,
                walk_completed=False,
                date=request.date,
                time=request.time,
                start_location_name=request.location_name,
                start_location_latitude=request.loc_lat,
                start_location_longitude=request.loc_long,
                payment_id = int(id)
            )

             # Update order in DB
            order = PaymentOrder.objects.get(order_id=razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.signature = razorpay_signature
            order.status = "paid"

            request.fees_paid = True
            request.walker.total_earning += 500

            request.wanderer.total_charity += 50
            
            order.save()
            request.walker.save()
            request.wanderer.save()
            
            request.save()

            # Walker notification
            async_to_sync(sendNotifications)(
                user_id=request.walker.user.id,
                title="New Walk Booked",
                body=(
                    f"Your walk with {request.wanderer.user.name} "
                    "has been confirmed. Payment received successfully."
                )
            )

            # Wanderer notification
            async_to_sync(sendNotifications)(
                user_id=request.wanderer.user.id,
                title="Payment Successful",
                body=(
                    f"Your walk with {request.walker.user.name} "
                    "is confirmed. We'll see you at the scheduled time!"
                )
            )


            return Response({"status": "Payment verified successfully"}, status=status.HTTP_200_OK)

        except PaymentOrder.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(str(e))
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_detail(request,payment_id):
    try:
        try:
            payment = PaymentOrder.objects.get(id=payment_id)
        except PaymentOrder.DoesNotExist:
            return Response({"detail": "Payment does not exist"}, status=status.HTTP_403_FORBIDDEN)
        
        data = {
            "payment_id": payment.payment_id,
            "status": payment.status,
            "amount":payment.amount/100,
            "timestamp": str(payment.updated_at)
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)