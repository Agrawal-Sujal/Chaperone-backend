import logging
import os
from .models import FCMToken
import firebase_admin
from firebase_admin import credentials, messaging
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from chaperone.settings import BASE_DIR
import json

# from dotenv import load_dotenv
# load_dotenv(os.path.join(BASE_DIR, '.env'))

from chaperone.settings import BASE_DIR
import os

if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.path.join(BASE_DIR, "firebase-adminsdk.json")
    )
    firebase_admin.initialize_app(cred)

# FCM_CRED = os.getenv('FCM_CRED')

# if not FCM_CRED:
#     raise RuntimeError("FCM_CRED not set in environment")

# Initialize Firebase Admin SDK (do this once at module level)
# try:
#     fcm_cred = json.loads(FCM_CRED)
#     cred = credentials.Certificate(fcm_cred)
#     firebase_admin.initialize_app(cred)
# except ValueError:
#     # App already initialized
#     pass
# except FileNotFoundError:
#     pass
# if not firebase_admin._apps:
#     fcm_cred = json.loads(FCM_CRED)
#     cred = credentials.Certificate(fcm_cred)
#     firebase_admin.initialize_app(cred)

async def sendNotifications(user_id, title, body):
    try:
        # ✅ Fetch ONLY unique tokens
        tokens = await sync_to_async(list)(
            FCMToken.objects
            .filter(user_id=user_id)
            .values_list('token', flat=True)
            .distinct()
        )

        if not tokens:
            return True

        message = messaging.MulticastMessage(
            data={
                "title": title,
                "body": body,
            },
            tokens=list(tokens),  # ensure list
        )

        await sync_to_async(
            messaging.send_each_for_multicast
        )(message)

        return True

    except Exception as e:
        print("FCM Error:", e)
        return False

