from django.urls import path
from .views import *

urlpatterns = [
    path("create-order/", CreateOrderView.as_view(), name="create-order"),
    path("verify-order/",VerifyOrderView.as_view(),name = "verify-order"),
    path("get-payment-detail/<int:payment_id>/",get_payment_detail,name = "get_payment_detail")
]
