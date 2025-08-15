from django.urls import path

from .views import AuthencationStockExchagesView

urlpatterns = [
    path('vps', AuthencationStockExchagesView.as_view(), name='vps-authencation-otp'),
]
