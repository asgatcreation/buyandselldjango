from django.urls import path
from . import views

urlpatterns = [
   path("paystack/",views.initiate_payment, name="initiatepayment"),
   path('<str:ref>/', views.verify_payment, name="verify-payment")
]
  