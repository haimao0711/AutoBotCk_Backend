from django.urls import path
from . import views

urlpatterns = [
    path('', views.TransactionLogViews.as_view(), name='transaction-logs'),
]
