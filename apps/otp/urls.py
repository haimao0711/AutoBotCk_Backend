from django.urls import path
from . import views

urlpatterns = [
    path('bot/request-otp', views.bot_request_otp,
         name='request_otp'),
    path('bot/get-otp', views.bot_get_otp,
         name='get_otp'),
    path('user/bot-otp-status', views.get_status_bot_request_otp,
         name='user-get_otp'),
    path('user/send-otp', views.send_otp,
         name='send_otp'),
]
